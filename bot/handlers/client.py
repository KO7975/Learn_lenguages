import requests
import io
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base import mysql_con
from create_bot import (
    dp,
    bot,
    host,
    my_admin,
    bot_link,
    contact_tel,
    email,
    facebook,
)
from keyboards.client_kb import (
    kb_client1,
    kb_client2,
    inkb,
    to_teacher,
    courses,
    material_kb,
    courses_kb,
)


phone_number = ''
user_from_db = []

# #emojis
teacher_em =u'\U0001F469'
arr_down_em = u'\U00002b07'
arr_right_em =u'\U000027a1'
arr_left_em = u'\U00002b05'
arr_up_em = u'\U000023EB'

"""Client side"""
#give bottons acces

# Define a handler for new chat members
# @dp.message_handler(content_types=['new_chat_members'])
async def new_chat_members_handler(message: types.Message):
    for user in message.new_chat_members:
        # Send a welcome message with the "/start" button to the new user
        start_message = f"Hello {user.full_name}! I am a chatbot here to assist you with any questions or concerns you may have. To get started, please click the \"/button\" button below.{arr_down_em}"
        start_button = types.KeyboardButton("/button")
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
        await bot.send_message(chat_id=user.id, text=start_message, reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)


# Define a handler for the "/start" command
# @dp.message_handler(commands=['start_phone'])
async def contact(message: types.Message):
    # Create a new message with the "Request contact" button
    start_message = f"Please provide your phone number by clicking the \n\"Request contact\" button below."
    request_contact_button = types.KeyboardButton(text="/Request_contact", request_contact=True)
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(request_contact_button)
    await bot.send_message(chat_id=message.chat.id, text=start_message, reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)


# Define a handler for receiving a user's phone number
# @dp.message_handler(content_types=['contact'])
async def contact_handler(message: types.Message):
    global phone_number
    phone_number = message.contact.phone_number
    await mysql_con.CourseData.save_phone(message, phone_number)
    await bot.send_message(chat_id=message.chat.id, text=f"Thank you for providing your phone number: {phone_number}")
    await commands_start(message)


# @dp.message_handler(commands=['update'])
async def commands_start(message: types.Message):
    global aprowed_user_from_db

    aprowed_user_from_db = await mysql_con.CourseData.uprowed_user_from_db(message)

    from_db = await mysql_con.CourseData.user_from_db(message)
    if len(from_db) == 0:
        await mysql_con.write_user(message)
        from_db
    if len(from_db) > 0:
        if len(aprowed_user_from_db) > 0:
 
            if aprowed_user_from_db[0][0] == 1:
                await bot.send_message(message.from_user.id, f'Press /Your_course_data and begin to stady!{arr_down_em}', reply_markup=kb_client2)
                await message.delete()

            elif aprowed_user_from_db[0][0] == 0:
                await bot.send_message(message.from_user.id, f'\u203C \U000026D4 You haven\'t acces yet! \U000026D4 \u203C\nPlease contact your teacher {arr_down_em}', reply_markup=to_teacher)
                await bot.send_message(message.from_user.id, f'Use the buttons below for more information{arr_down_em}', reply_markup=kb_client1)
                await message.delete()
        else:
            await bot.send_message(message.from_user.id, f'You can find several buttons below for more information{arr_down_em}', reply_markup=kb_client1)
            await message.delete()
    else:
        await message.reply(f'Write any message to bot: \n{bot_link}')


#show course data from db for autorized user
# @dp.message_handler(commands=['Your course data'])
async def course_data(message: types.Message):
    global course, lesons, materi, addition_mat 
    course, lesons , materi, addition_mat = await mysql_con.CourseData.course_from_db(aprowed_user_from_db[0][2])
    if len(lesons) > 0 and len(course) > 0:
        await bot.send_message(message.from_user.id, f'Your course {course[0][3]} lessons: ')
        n = 1
        for i in lesons:
            await bot.send_message(message.from_user.id,f"Lesson{n} ---\U00002b07---", reply_markup= courses(i[1], i[0], f'ls_{i[1]}'))       
            n+=1
        n = 1
    if len(addition_mat) > 0:
        for mat in addition_mat:
            # await download_photo_handler(calback, mat[2], mat[4], mat[1], mat[5], mat[6])
            await bot.send_message(message.from_user.id, f"Addition material: {mat[4]}\n\U00002b07", reply_markup=material_kb(mat[4], f'amt_{mat[4]}'))
    else:
        await bot.send_message(message.from_user.id, "You don\'t have any materials for You.\nPlease contact your teacher\n", reply_markup=to_teacher)
    await message.delete()


async def download_photo_handler(message, url, title, material_type, text, URL):
    # Set the material URL
    if material_type == 'url':
        await bot.send_message(
            chat_id=message.message.chat.id,
            text=f'{text}\nUse link {arr_down_em}',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=title, url=URL)))
    elif material_type == 'text':
        await bot.send_message(chat_id=message.message.chat.id, text=text)

    elif material_type == 'photo':
        # Download the photo from the URL
        file_url = f'{host}en/{url}'
        file_request = requests.get(file_url, params=url)
        code = file_request.status_code
        content = file_request.content

        if code != 200:
            await bot.send_message(chat_id=message.message.chat.id, text=f"Failed to download file: {code}")
            return
        # Send the photo to Telegram
        file_bytes = io.BytesIO(content)
        file = types.InputFile(file_bytes, filename=title)
        await bot.send_photo(chat_id=message.message.chat.id, caption=text, photo=file)
    else:
        link = f'{host}en/materials/course/{course[0][0]}'

        await bot.send_message(
            chat_id=message.message.chat.id,
            text=f'{text}\nUse link {arr_down_em}',
            reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text=title, url=link)))



# @dp.callback_handler(commands=['ls_'])
async def lessons(message: types.CallbackQuery):
    res = await mysql_con.CourseData.new(aprowed_user_from_db[0][2])
    for i in lesons:
        for l in res:
            if message.data.endswith(i[1]) and i[2] == l[1]:
                for mat in materi:
                    if l[0]==mat[0]:
                        await download_photo_handler(message, mat[2], mat[4], mat[1], mat[5], mat[6])
    

# @dp.callback_handler(Text(startswith='amt_')
async def materials(message: types.CallbackQuery):
    for mat in addition_mat:
        if message.data.endswith(mat[4]):
            await download_photo_handler(message, mat[2], mat[4], mat[1], mat[5], mat[6])


#show working hours
# @dp.message_handler(commands=['Working_time'])
async def work_time(message: types.Message):
    await bot.send_message(message.from_user.id, 'Monday - Friday 9:00 to 19:00')
    await message.delete()


#show languages-bottons that user can chouse
async def languages_to_learn(message: types.Message):
    global ans
    ans = await mysql_con.my_db_read(message)
    if type(ans)==tuple:
        await message.answer(f'There are languages that you can stady: {arr_down_em}\n') 
        for i in ans:
            await bot.send_message(
                message.from_user.id,
                text='↓', \
                reply_markup=courses_kb(f'{i[1]}', f'ab_{i[1][1:5]}'))


# @dp.callback_handler(Text(startswith='ab_')
async def course_buttons(callback: types.CallbackQuery):
    for i in ans:
        if callback.data.endswith(i[1][1:5]):
            await bot.send_photo(callback.from_user.id, i[0], f'Name: {i[1]}\nDescription:{i[2]}' )


async def inform(message: types.CallbackQuery):
    await bot.send_message(
        message.from_user.id,
        text=f'If you didn\'t found your target language {arr_up_em} You can write me language that You want to learn and I will try to help you',\
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Write Your question',
        url=my_admin,
        callback_data='inf'))
        )
    await message.answer (f'You can write me a private message')


async def price(message: types.Message):
    await bot.send_message(message.from_user.id, f'Price per 1 hour is 300 UAH')
    await message.delete()


async def contacts(message: types.Message):
    await bot.send_message(
        message.from_user.id,
        f'There are contacts:\n📲 {contact_tel}\n📧 {email}\nfacebook {facebook}\nets',
        #reply_markup=ReplyKeyboardRemove(), #remove keyboard
        )
    await message.delete()


# dp.message_handler(commands=['All Courses'])
async def all_courses(message: types.Message):
    await mysql_con.my_db_read(message)
    await message.delete()


# @dp.callback_query_handler(Text(startswith='ln_'))
async def chuse(callback: types.CallbackQuery):
    await mysql_con.DbLike(callback).write()
    await bot.send_message(callback.from_user.id,'Thank you for your choice.')


#dp.mesage_handler(commands=['like'])
async def test_command(message: types.Message):
    likes, dislikes = await mysql_con.show_likes()
    inlkb = InlineKeyboardMarkup(row_width=1)\
    .add(InlineKeyboardButton(text=f'\U0001F44D {likes[0][0]} ', callback_data='ln_1'))\
    .add(InlineKeyboardButton(text=f'\U0001F44E {dislikes[0][0]}', callback_data='ln_2'))
    await message.answer('Do you like this bot?', reply_markup=inlkb)
    await message.delete()
    

#registretion all battons
def registr_handlers_client(dp: Dispatcher):
    dp.register_message_handler(new_chat_members_handler,content_types=['new_chat_members'])
    dp.register_message_handler(contact, commands=['button'])
    dp.register_message_handler(commands_start, commands=['update', 'start', 'help'])
    dp.register_message_handler(work_time, commands=['Working_time⌚'])
    dp.register_message_handler(languages_to_learn, commands=['Course_list\U0001F4D1'])
    dp.register_message_handler(price, commands=['💰price'])
    dp.register_message_handler(contacts, commands=['contacts💬'])
    dp.register_message_handler(all_courses, commands=['All_Courses\U0001F4DA'])
    dp.register_message_handler(test_command, commands=['like'])
    dp.register_message_handler(contact_handler, content_types=['contact'])
    dp.register_message_handler(course_data, commands=['Your_course_data'])

    dp.register_callback_query_handler(materials, Text(startswith='amt_'))
    dp.register_callback_query_handler(lessons, lambda c: c.data.startswith('ls_'))
    dp.register_callback_query_handler(chuse, Text(startswith='ln_'))
    dp.register_callback_query_handler(inform, text=['rm'])
    dp.register_callback_query_handler(course_buttons, Text(startswith='ab_'))

