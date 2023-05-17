from aiogram import types, Dispatcher
from create_bot import dp
import json, string


# @dp.message_handler()
async def echo_send(message: types.Message):

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
    .intersection(set(json.load(open('cenz.json')))) != set():
        await message.reply(f'{message.from_user.username}! You can\'t use such swear words!')
        await message.delete()

    if message.text == 'hello':
        await message.reply(f'Hello {message.from_user.username}! Nice to see you here')
    #sent simple answer
    # await message.answer('Hello')

    #reply with your massage
    # await message.reply(message.text)

    #sent masseg to user
    #await bot.send_message(message.from_user.id, f'hello user: {message.from_user.id}')  

def registr_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)

