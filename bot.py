from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

bot = TelegramBot(api_token)
offset = None

def print_update_cb(update):
    print(update.message.text.strip())

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

def process_updates(callback=print_update_cb, timeout=0):
    global offset
    updates = bot.get_updates(offset=offset,timeout=0).wait()
    for update in updates:
        callback(update)
        offset = update.update_id + 1

while True:
    process_updates(callback=print_and_reverse_cb, timeout=1)
