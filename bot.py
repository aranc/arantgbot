from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = _file.readline().strip()

bot = TelegramBot(api_token)
offset = None

def print_and_reverse_cb(update):
    try:
        user_id = update.message.sender.id
        msg = update.message.text.strip()
    except:
        print "caught exception for update:"
        print update
        print
        return
    print str(user_id) + ": " + msg
    bot.send_message(user_id, "".join(reversed(msg))).wait()

def process_updates_callback(update):
    try:
        user_id = update.message.sender.id
        msg = update.message.text.strip()

        if user_id != my_user_id:
            return print_and_reverse_cb(update)

        cmd = msg.split()[0:1]
        parameters = "".join(msg.split()[1:])
        print "<"+cmd+">: "+"<"+parameters+">"
        for registered_command in registered_commands:
            

    except:
        print "caught exception for update:"
        print update
        print
        return
    
def process_updates(callback=print_update_cb, timeout=0):
    global offset
    updates = bot.get_updates(offset=offset,timeout=0).wait()
    for update in updates:
        callback(update)
        offset = update.update_id + 1

def go_online():
    while True:
        process_updates(callback=process_updates_callback, timeout=1)

registered_commands = {}
def register_command(cmd, cb):
    registered_commands[cmd] = cb

if __name__ == "__main__":
    while True:
        process_updates(callback=print_and_reverse_cb, timeout=1)
