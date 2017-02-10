#!/usr/bin/python
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = int(_file.readline().strip())

with open(os.path.expanduser(sys.argv[1]), 'r') as _file:
    msg = _file.read()

bot = TelegramBot(api_token)
bot.send_message(my_user_id, msg).wait()
