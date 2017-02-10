#!/usr/bin/python
from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import sys
import os
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = int(_file.readline().strip())

bot = TelegramBot(api_token)
bot.send_message(my_user_id, " ".join(sys.argv[1:])).wait()
