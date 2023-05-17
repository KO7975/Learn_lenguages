from aiogram import types, Dispatcher
from create_bot import dp, bot, host, my_admin, bot_link, contact_tel, email, facebook
from keyboards.client_kb import kb_client1, kb_client2, inkb, inlkb, to_teacher, courses, material_kb
from data_base import mysql_con
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import  ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
import requests
import io
import os

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
        start_message = f"Hello {user.full_name}! I am a chatbot here to assist you with any questions or concerns you may have. To get started, please click the \"/start\" button below.{arr_down_em}"
        start_button = types.KeyboardButton("/start_phone")
        reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(start_button)
        await bot.send_message(chat_id=user.id, text=start_message, reply_markup=reply_markup, parse_mode=types.ParseMode.HTML)


# Define a handler for the "/start" command
# @dp.message_handler(commands=['start_phone'])
async def contact(message: types.Message):
    # Create a new message with the "Request contact" button
    start_message = f"Please provide your phone number by clicking the \"Request contact\" button below."
    request_contact_button = types.KeyboardButton(text="/Request contact", request_contact=True)
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
        await mysql_con.DbLike(message).write()
    if len(from_db) > 0:
        if len(aprowed_user_from_db) > 0:
            if aprowed_user_from_db[0][0] == 1:
                await bot.send_message(message.from_user.id, f'Press /Your_course_data and begin to stady!{arr_down_em}', reply_markup=kb_client2)
                await message.delete()
            # elif len(from_db) > 0:
            elif aprowed_user_from_db[0][0] == 0:
                await bot.send_message(message.from_user.id, f'\u203C \U000026D4 You haven\'t acces yet! \U000026D4 \u203C\nPlease contact your teacher {arr_down_em}', reply_markup=to_teacher)
                await bot.send_message(message.from_user.id, f'Touch the buttons below for more information{arr_down_em}', reply_markup=kb_client1)
                await message.delete()
            else:
                await bot.send_message(message.from_user.id, f'You can find several buttons below for more information{arr_down_em}', reply_markup=kb_client1)
                await message.delete()
                # await bot.send_message(message.from_user.id, f'You can find several buttons below for more information{arr_down_em}', reply_markup=kb_client1)
                # await message.delete()
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

    else:
        ##If your bot in the same machine with web broject
        # url = url.replace('/', os.sep)
        # print(url)
        # file_url = rf"C:\Users\Nadiia\Desktop\English_site\progect\english_learning\media\{url}"
        # file_f = open(file_url, 'rb')
        # file_bytes = file_f.read()
        # file_f.close()
        # file_bytes = io.BytesIO(file_bytes)
        # file = types.InputFile(file_bytes, filename=title)
 
        # Download the photo from the URL from different machine
        file_url = f'{host}{url}'
        # file_url = f'C:\Users\Nadiia\Desktop\English_site\progect\english_learning\{url}'
        file_request = requests.get(file_url, params=url, data=url)
        if file_request.status_code != 200:
            await bot.send_message(chat_id=message.message.chat.id, text=f"Failed to download file: {file_request.status_code}")
            return

        # Send the photo to Telegram
        file_bytes = io.BytesIO(file_request.content)
        file = types.InputFile(file_bytes, filename=title)
        if material_type == 'photo':
            await bot.send_photo(chat_id=message.message.chat.id,caption=text, photo=file)
        elif material_type == 'video':
            await bot.send_video(chat_id=message.message.chat.id,caption=text, video=file)
        elif material_type == 'audio':
            await bot.send_audio(chat_id=message.message.chat.id,caption=text, audio=file)



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
async def languages_to_learn(message: types.CallbackQuery):
    await message.answer(f'There are languages that you can stady: {arr_down_em}\n', reply_markup=inkb) 
    # await mysql_con.my_db_read_lang(message)
    await message.delete()


async def process_callback_button1(callback: types.CallbackQuery):
    await bot.send_message(
        callback.from_user.id,
        text=f"Read more about course {arr_down_em} ",
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='About',callback_data='ab_en'))
        )
    await callback.answer('botton pressed!', show_alert=True)        # desaphired answer   with show_alert=True opened window with alert


async def process_callback_button2(callback: types.CallbackQuery):
    await bot.send_message(
        callback.from_user.id,
        text=f'Read more about course {arr_down_em}',
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='About',callback_data='ab_sp'))
        )
    await callback.answer('botton pressed!', show_alert=True)        # desaphired answer   with show_alert=True opened window with alert
 
async def process_callback_button3(callback: types.CallbackQuery):
    await bot.send_message(
        callback.from_user.id,
        text=f'Read more about course {arr_down_em}',
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='About',callback_data='ab_ps'))
        )
    await callback.answer('botton pressed!', show_alert=True)        # desaphired answer   with show_alert=True opened window with alert


async def process_callback_button4(callback: types.CallbackQuery):
    await bot.send_message(
        callback.from_user.id,
        text=f'Read more about course {arr_down_em}',
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='About',callback_data='ab_en_s'))
        )
    await callback.answer('botton pressed!', show_alert=True)        # desaphired answer   with show_alert=True opened window with alert



async def inform(message: types.CallbackQuery):
    await bot.send_message(
        message.from_user.id,
        text=f'If you didn\'t found your target language {arr_up_em} You can write me language that You want to learn and I will try to help you',\
        reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Write Your question',
        url=my_admin,
        callback_data='inf'))
        )
    await message.answer (f'You can write me a private message')


# Get description language from db with function
# async def description_en(callback: types.CallbackQuery):
#     await mysql_con.Description(callback, 'English').get_desc()


# Get description language from db with class method
class LangDescription():
    def __init__(self, name, ) -> None:
        self.name = name
    async def desc_lang(self, callback):
        await mysql_con.Description(callback, self.name).get_desc()


description_en = lambda callback=types.CallbackQuery: LangDescription('English').desc_lang(callback)
description_sp = lambda callback=types.CallbackQuery: LangDescription('Spanish').desc_lang(callback)
description_ps = lambda callback=types.CallbackQuery: LangDescription('Polish').desc_lang(callback)
description_ens = lambda callback=types.CallbackQuery: LangDescription('English for seamen').desc_lang(callback)


async def price(message: types.Message):
    await bot.send_message(message.from_user.id, f'Price per 1 hour is 300 UAH')
    await message.delete()

# async def get_contact(message: types.Message, state: FSMContext):
#     await message.answer(f'phone: {message.contact.phone_number}')
#     await state.finish()


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
    


#dp.mesage_handler(commands=['like'])
async def test_command(message: types.Message):
    await message.answer('Do you like this bot?', reply_markup=inlkb)
    await message.delete()
    await mysql_con.DbLike(message).show_likes()


#registretion all battons
def registr_handlers_client(dp: Dispatcher):
    dp.register_message_handler(new_chat_members_handler,content_types=['new_chat_members'])
    dp.register_message_handler(contact, commands=['start_phone'])
    dp.register_message_handler(commands_start, commands=['update', 'start'])
    dp.register_message_handler(work_time, commands=['Working_time⌚'])
    dp.register_message_handler(languages_to_learn, commands=['Course_list\U0001F4D1'])
    dp.register_message_handler(price, commands=['💰price'])
    dp.register_message_handler(contacts, commands=['contacts💬'])
    dp.register_message_handler(all_courses, commands=['All_Courses\U0001F4DA'])
    dp.register_message_handler(test_command, commands=['like'])
    dp.register_message_handler(contact_handler, content_types=['contact'])
    dp.register_message_handler(course_data, commands=['Your_course_data'])
    # dp.register_message_handler (lessons, commands=['ls'])

    dp.register_callback_query_handler(materials, Text(startswith='amt_'))
    dp.register_callback_query_handler(lessons, lambda c: c.data.startswith('ls_'))
    dp.register_callback_query_handler(chuse, Text(startswith='ln_'))
    dp.register_callback_query_handler(process_callback_button1, text=['en'])
    dp.register_callback_query_handler(process_callback_button2, text=['sp'])
    dp.register_callback_query_handler(process_callback_button3, text=['ps'])
    dp.register_callback_query_handler(process_callback_button4, text=['en_s'])
    dp.register_callback_query_handler(inform, text=['rm'])
    dp.register_callback_query_handler(description_en, text=['ab_en'])
    dp.register_callback_query_handler(description_sp, text=['ab_sp'])
    dp.register_callback_query_handler(description_ps, text=['ab_ps'])
    dp.register_callback_query_handler(description_ens, text=['ab_en_s'])

