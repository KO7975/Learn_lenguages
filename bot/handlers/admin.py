from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from data_base import mysql_con
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()

#Get ID of moderator
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_commands(message: types.Message):
    global ID 
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Hello my Lord',reply_markup=admin_kb.button_case_admin)
    await message.delete()


#Begining of the dialog and downloading new menu item
# @dp.message_handler(commands='Download', state=None)
async def cm_start(message: types.Message):
    # chack that user is admin
    print(ID)
    if message.from_user.id == ID: 
        await FSMAdmin.photo.set()
        await message.reply('downloud the photo')


#Catch first answer from user and save to dictionary
# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id

        await FSMAdmin.next()
        await message.reply('Now add name')


#Catch next answer from user and save to dict
# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Enter description')

#Catch next answer from user and save to dict
# @dp.message_handler(state=FSMAdmin.description)
# async def load_description(message: types.Message, state:FSMContext):
#     if message.from_user.id == ID:
#         async with state.proxy() as data:
#             data['description'] = message.text
#         await FSMAdmin.next()
        

#Catch last answer from user and save to dict and leave seanse
# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state:FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await mysql_con.my_db_add_command(state)
        await message.reply('Loaded to DB')
        # async with state.proxy() as data:
        #     await message.reply(str(len(tuple(data.values())[0])))
        #sql_add(state)
        await state.finish()


# @dp.message_handler(state="*", commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        curent_state = await state.get_state()
        if curent_state is None:
            return
        await state.finish()
        await message.reply('OK')


# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback: types.CallbackQuery):
    await mysql_con.my_db_delete(callback.data.replace("del ", ""))
    await callback.answer(text=f"{callback.data.replace('del ', '')} deleted.", show_alert=True)


# @dp.message_handler(commands=['Delete'])
async def delete_lang(message: types.Message):
    if message.from_user.id == ID:
        read = await mysql_con.my_db_read2()
        for i in read:
            await bot.send_photo(message.from_user.id, i[0], f'Language: {i[1]}\nDescription:{i[2]}')
            await bot.send_message(message.from_user.id, text="^^^",reply_markup=InlineKeyboardMarkup().\
                                   add(InlineKeyboardButton( f'Delete {i[1]}', callback_data=f'del {i[1]}')))


def registr_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['download'], state=None)
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(cancel_handler, state="*", commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(make_changes_commands, commands=['moderator'], is_chat_admin=True)
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    dp.register_message_handler(delete_lang, commands=['Delete'])