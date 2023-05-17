
# import asyncio
# from telebot.async_telebot import AsyncTeleBot
# # from telegram_menu import BaseMessage, TelegramMenuSession, NavigationHandler
# import telebot
# import pymysql
# from telebot import types



# bot = telebot.TeleBot('6096355050:AAEgZHfIr7WQDQ7s0uEIGZRgp-oLBD31Nrk')

# # bot.infinity_polling(interval=0, timeout=10)
# user = bot.get_me()
# print(user)
# updates = bot.get_updates(1234,100,10)




# bot.send_message(chat_id='-819264347',text='Hello')

# # markup = types.ReplyKeyboardMarkup()
# # itembtna = types.KeyboardButton('a')
# # itembtnv = types.KeyboardButton('v')
# # itembtnc = types.KeyboardButton('c')
# # itembtnd = types.KeyboardButton('d')
# # itembtne = types.KeyboardButton('e')
# # markup.row(itembtna, itembtnv)
# # markup.row(itembtnc, itembtnd, itembtne)
# # bot.send_message(chat_id='-819264347', text="Choose one letter:", reply_markup=markup)

# # # Handle '/start' and '/help'
# # @bot.message_handler(commands=['help', ])
# # def send_welcome(message):
# #     bot.reply_to(message, """\
# # Hi there, I am EchoBot.
# # I am here to echo your kind words back to you. Just say anything nice and I'll say the exact same thing to you!\
# # """)

# # @bot.message_handler(func=key_bourd, commands=['new',])
# # def sent_massage(massage):
# #      bot.send_message(chat_id='-819264347')

# # #Handle all other messages with content_type 'text' (content_types defaults to ['text'])
# # # @bot.message_handler(func=lambda message: True)
# # # async def echo_message(message):
# # #     await bot.reply_to(message, message.text)

# def connection_to_db():
#         conn = pymysql.connect( host='mysql', user='mydatabaseuser', passwd='12345', db="mydatabase" )
#         crsr = conn.cursor()
#         sql_command= 'select name from materials_lesson;'
#         crsr.execute(sql_command)
#         for i in crsr:
#             return i

# crsr = connection_to_db()
# print(crsr[0])

# # @bot.message_handler(commands=['name',])
# # def from_db_massage(massage=crsr):
# #      bot.reply_to(massage, text=crsr[0])

# @bot.message_handler(commands=["start"])
# def start_command(message):
#     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
#     button1 = types.KeyboardButton(text="Button 1")
#     button2 = types.KeyboardButton(text="Button 2")
#     button3 = types.KeyboardButton(text="Button 3")

#     keyboard.add(button1, button2, button3)
#     bot.send_message(chat_id='-819264347', text='Hello!', reply_markup=keyboard)

# # Here's a simple handler when user presses button with "Button 1" text
# @bot.message_handler(content_types=["text"], func=lambda message: message.text == "Button 1")
# async def func1(message):
#     keyboard = types.InlineKeyboardMarkup()
#     url_btn = types.InlineKeyboardButton( text="Go to Lessons")
#     keyboard.add(url_btn)
#     await bot.answer_inline_query(chat_id='-819264347', switch_pm_text="Button 1 handler", reply_markup=keyboard)

# bot.infinity_polling()
# # asyncio.run(bot.polling())

import requests
import telegram
import mysql.connector
from extractor_phone_email import extractor
# from peewee import *
# from playhouse.reflection import generate_models

# Connect to the MySQL database

db = mysql.connector.connect(
    host="mysql",
    user="mydatabaseuser",
    password="12345",
    database="mydatabase"
)

# Create a cursor object to execute queries
cursor = db.cursor()


# Set up the Telegram bot with your API token
token = '6096355050:AAEgZHfIr7WQDQ7s0uEIGZRgp-oLBD31Nrk'
bot = telegram.Bot(token=token)


# Define a function to get the user's phone number by user ID
def get_phone_number(user_id):
    # Get the user's profile photos
    photos = bot.get_user_profile_photos(user_id)

    # If the user has profile photos, get the last photo
    if photos.total_count > 0:
        last_photo = photos.photos[-1][-1]

        # Get the file ID of the last photo
        file_id = last_photo.file_id

        # Use the file ID to get the file object
        file = bot.get_file(file_id)

        # Get the file path of the file object
        file_path = file.file_path

        # Construct the URL for the file
        url = f'https://api.telegram.org/file/bot{bot.token}/{file_path}'

        # Make a request to the Telegram API to download the file
        response = requests.get(url)

        # Use the myExtractor library to extract the phone number from the file contents
        myExtractor = extractor.Extractor(response.content)
        phone_number = myExtractor.get_phones()

        return phone_number[0]

    # If the user doesn't have profile photos, return None
    else:
        return None

# Define a function to handle the user's messages and button presses
def handle_message(update, context):
    # Get the user ID
    user_id = update.message.from_user.id

    # Get the user's phone number
    phone_number = get_phone_number(user_id)
    # phone_number = '0987654321'

    # If the user's phone number is in the database
    if phone_number is not None:
        cursor.execute(f"SELECT courses_id FROM materials_userprofile WHERE phone_number='{phone_number}' AND is_approved=True")
        course_id = cursor.fetchall()
        # Get the user's lessons or materials, depending on which button they pressed
        if update.message.text == 'Lessons':
            lessons = course_id[0].lesson1.all()         
            # cursor.execute(f"SELECT lesson FROM materials_lesson WHERE phone_number='{phone_number}'")
            # lessons = cursor.fetchall()
            lesson_list = [lesson for lesson in lessons]
            message = 'Your lessons:\n' + '\n'.join(lesson_list)
        else:
            message = "Please select either 'Lessons' or 'Materials'."

    # If the user's phone number is not in the database
    else:
        message = 'Please add your phone number to the database.'

    # Send the message to the user
    update.message.reply_text(message, reply_markup=telegram.ReplyKeyboardRemove())

# Set up the Telegram bot updater and dispatcher
updater = telegram.ext.Updater(token='your_api_token', use_context=True)
dispatcher = updater.dispatcher

# Register the message handler function
dispatcher.add_handler(telegram.ext.MessageHandler(
    telegram.ext.Filters.text, handle_message))

# Set up the keyboard with the 'Lessons' and 'Materials' buttons
keyboard = [['Lessons'], ['Materials']]
reply_markup = telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)

# Start the bot
updater.start_polling()




