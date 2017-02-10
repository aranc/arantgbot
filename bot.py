#!/usr/bin/python
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = _file.readline().strip()

log = open(os.path.expanduser("~/arantgbot.log"), 'a')

bot = TelegramBot(api_token)
offset = None

def process_updates_callback(update):
    try:
        user_id = update.message.sender.id
        msg = update.message.text.strip()

        print str(user_id) + ": " + msg
        log.write(str(user_id) + ": " + msg + "\n")
        log.flush()

        if user_id != my_user_id:
            bot.send_message(user_id, "".join(reversed(msg))).wait()
            return

        cmd = msg.split()[0:1]
        parameters = "".join(msg.split()[1:])
        if cmd in registered_commands:
            response = registered_commands[cmd](cmd, parameters)
            if isinstance(response, basestring): #Change to str in python3
                bot.send_message(user_id, response).wait()
        else:
            bot.send_message(user_id, "".join(reversed(msg))).wait()
            
    except:
        print "caught exception for update:"
        print update
        print
        return
    
def process_updates(callback, timeout=0):
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
    go_online()
