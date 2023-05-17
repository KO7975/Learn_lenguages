from aiogram.utils import executor
from create_bot import dp
from data_base import mysql_con
from handlers import client, admin, other


# here we can make connaction to db
async def on_startup(_):
    print('Bot is online')
    await mysql_con.db_start()


client.registr_handlers_client(dp)
admin.registr_handlers_admin(dp)
other.registr_handlers_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)