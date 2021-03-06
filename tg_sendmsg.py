#!/usr/bin/env python3
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import sys
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = int(_file.readline().strip())

bot = TelegramBot(api_token)
msg = " ".join(sys.argv[1:])
msg = msg.replace('\\n', '\n')
bot.send_message(my_user_id, msg).wait()
