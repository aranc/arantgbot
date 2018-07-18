#!/usr/bin/python3
from twx.botapi import TelegramBot, ReplyKeyboardMarkup, InputFileInfo, InputFile
import os
import sys
import time

with open(os.path.expanduser("~/arantgbot.api_token"), 'r') as _file:
    api_token = _file.readline().strip()

with open(os.path.expanduser("~/arantgbot.my_user_id"), 'r') as _file:
    my_user_id = int(_file.readline().strip())

bot = TelegramBot(api_token)
fp = open(os.path.expanduser(sys.argv[1]), 'rb')
file_info = InputFileInfo(sys.argv[1], fp, 'image/png')
inputfile=InputFile('photo', file_info)
bot.send_photo(chat_id=my_user_id, photo=inputfile)
