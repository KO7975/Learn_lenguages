from  aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from dotenv import load_dotenv
from aiogram.contrib.fsm_storage.memory import MemoryStorage #help keep data in random access memory


load_dotenv()

storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=storage)

#host of web project
host = os.getenv('HOST')

#admin private telegram profile
my_admin = os.getenv("MY_ADMIN")
bot_link= os.getenv("BOT_LINK")
contact_tel= os.getenv('CONTACT_TEL')
email= os.getenv("EMAIL")
facebook= os.getenv('FACEBOOK')

