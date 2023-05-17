from  aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage #help keep data in random access memory


storage = MemoryStorage()
# bot = Bot(token=os.getenv('TOKEN'))
bot = Bot(token='6096355050:AAEgZHfIr7WQDQ7s0uEIGZRgp-oLBD31Nrk')
dp = Dispatcher(bot, storage=storage)

#host of web project
host = "http://localhost:80/"
#admin private telegram profile
my_admin = "https://t.me/@Pirat17"
bot_link='https://t.me/std_lang_bot'
contact_tel='+380987654321'
email='example@mail.com'
facebook='https://www.facebook.com/staciewhite22'
