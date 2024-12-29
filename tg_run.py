#!/usr/bin/env python3
import os
import sys
import pexpect
import time
from twx.botapi import TelegramBot
import threading
from queue import Queue
import argparse

class ProgramWrapper:
    def __init__(self, command: str):
        self.command = command
        self.process = None
        self.output_queue = Queue()
        self.start_program()

    def start_program(self):
        """Start the wrapped program using pexpect"""
        try:
            print(f"Starting program: {self.command}")
            self.process = pexpect.spawn(self.command, encoding='utf-8', timeout=None)
            self.process.logfile_read = sys.stdout  # Debug: See all output
            threading.Thread(target=self._monitor_output, daemon=True).start()
            return True
        except Exception as e:
            print(f"Error starting program: {e}")
            return False

    def _monitor_output(self):
        """Monitor program output and put it in the queue"""
        while self.process is not None:
            try:
                index = self.process.expect(['\n', pexpect.EOF, pexpect.TIMEOUT], timeout=1)
                if index == 0:  # Got a line
                    line = self.process.before + '\n'
                    if line.strip():  # Only queue non-empty lines
                        print(f"Program output: {line.strip()}")
                        self.output_queue.put(line)
                elif index == 1:  # EOF
                    print("Program ended (EOF)")
                    break
            except Exception as e:
                print(f"Error monitoring output: {e}")
                break

    def send_input(self, text: str) -> bool:
        """Send input to the program"""
        if self.process is None or not self.process.isalive():
            print("Cannot send input - process not alive")
            return False
        try:
            print(f"Sending input to program: {text}")
            self.process.sendline(text)
            return True
        except Exception as e:
            print(f"Error sending input: {e}")
            return False

    def get_output(self):
        """Get output from the queue if available"""
        try:
            return self.output_queue.get_nowait()
        except:
            return None

class TelegramBotWrapper:
    def __init__(self, program_command: str, token_file: str):
        # Read configuration
        with open(os.path.expanduser(token_file), 'r') as f:
            self.api_token = f.readline().strip()
        with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as f:
            self.my_user_id = int(f.readline().strip())

        self.bot = TelegramBot(self.api_token)
        self.program = ProgramWrapper(program_command)
        self.offset = None
        
        # Start output monitoring right away
        self.start_output_monitoring(self.my_user_id)

    def process_updates_callback(self, update):
        """Process each update from Telegram"""
        try:
            user_id = update.message.sender.id
            msg = update.message.text.strip()
            print(f"Received message from {user_id}: {msg}")
            
            # Only respond to authorized user
            if user_id != self.my_user_id:
                self.bot.send_message(user_id, "Unauthorized").wait()
                return

            # Handle regular messages (program input)
            if self.program.process is None or not self.program.process.isalive():
                print("Program not alive, can't send input")
                self.bot.send_message(user_id, "Program has ended").wait()
                return

            self.program.send_input(msg)

        except Exception as e:
            print(f"Error in process_updates_callback: {e}")
            return

    def process_updates(self):
        """Get and process updates from Telegram"""
        updates = self.bot.get_updates(offset=self.offset, timeout=1).wait()
        for update in updates:
            self.process_updates_callback(update)
            self.offset = update.update_id + 1

    def start_output_monitoring(self, user_id: int):
        """Start monitoring program output"""
        def monitor():
            while self.program.process is not None and self.program.process.isalive():
                output = self.program.get_output()
                if output:
                    try:
                        print(f"Sending to Telegram: {output.strip()}")
                        self.bot.send_message(user_id, output).wait()
                    except Exception as e:
                        print(f"Error sending to Telegram: {e}")

        threading.Thread(target=monitor, daemon=True).start()

    def run(self):
        """Main bot loop"""
        print("Bot started, waiting for messages...")
        while True:
            try:
                self.process_updates()
                time.sleep(0.1)  # Prevent tight loop
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(1)  # Wait a bit before retrying
            except KeyboardInterrupt:
                print("Received KeyboardInterrupt, exiting...")
                break

def main():
    parser = argparse.ArgumentParser(description='Run a program with Telegram bot interface')
    parser.add_argument('--token-file', 
                      default='~/arantgchat.api_token',
                      help='Path to file containing Telegram bot token (default: ~/arantgchat.api_token)')
    parser.add_argument('command', nargs=argparse.REMAINDER,
                      help='Command to run (with any arguments)')

    args = parser.parse_args()

    if not args.command:
        parser.error("No command specified")

    # Construct the command from remaining arguments
    command = " ".join(args.command)
    
    # Create and run the bot
    bot = TelegramBotWrapper(command, args.token_file)
    bot.run()

if __name__ == "__main__":
    main()