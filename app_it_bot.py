from utils.db_api.database import create_db
from utils.db_api import sql_db
from utils.set_bot_commands import set_default_commands


async def on_startup(dp):
    # import filters
    # import middlewares
    # filters.setup(dp)
    # middlewares.setup(dp)
    await set_default_commands(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await create_db()
    # Создание и запуск БД SQL
    await sql_db.sql_start()

if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
