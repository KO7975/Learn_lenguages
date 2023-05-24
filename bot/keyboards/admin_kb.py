from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
all_courses = KeyboardButton('/Course_list\U0001F4D1')
button_load = KeyboardButton('/Download_course')
button_delete = KeyboardButton('/Delete_course')
button_all_users = KeyboardButton('/All_users')
up = KeyboardButton('/update')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard=True)\
    .add(all_courses).row(button_load, button_delete).add(button_all_users).add(up)


