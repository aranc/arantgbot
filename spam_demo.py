#!/usr/bin/env python3
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import sys
import os
import time

print "spam spawned"

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = int(_file.readline().strip())

bot = TelegramBot(api_token)
for i in range(100):
    time.sleep(1)
    msg = str(i) + " " + " ".join(sys.argv[1:])
    print "spammm:", msg
    bot.send_message(my_user_id, msg).wait()
