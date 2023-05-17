from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_load = KeyboardButton('/Download')
button_change = KeyboardButton('/Change')
button_delete = KeyboardButton('/Delete')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(button_load).add(button_change).add(button_delete)