import sqlite3 as sq

from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from loader import bot


async def sql_start():
    global base, cur
    base = sq.connect('market_shop.db')
    cur = base.cursor()
    if base:
        await bot.send_message(ADMINS, 'БАЗА ДАННЫХ ПОДКЛЮЧЕНА')
        base.execute('CREATE TABLE IF NOT EXISTS orders(pizza TEXT, name TEXT, number TEXT, address TEXT)')
        base.commit()


async def sql_add_orders(state):
    base = sq.connect('market_shop.db')
    cur = base.cursor()
    async with state.proxy() as data:
        cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?)", tuple(data.values()))
        base.commit()


async def sql_read_orders(message, data):
    # base = sq.connect('market_shop.db')
    # cur = base.cursor()
    # cur.execute('SELECT * FROM orders WHERE number=?', (data,))
    # results = cur.fetchall()
    # for i in results:
    name = data['name']
    product = data['product']
    volume = data['volume']
    number = data['number']
    time = data['time']
    await bot.send_message(ADMINS, f'Получен заказ\n{name} ({number})\n{product} ({volume})\n\n'
                                   f'Подготовить к {time}')
    # await bot.send_message(message.from_user.id, text='Принят заказ')