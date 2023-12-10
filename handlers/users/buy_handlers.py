import re
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from utils.db_api.db_commands import get_name_item
from utils.db_api.sql_db import sql_read_orders, sql_add_orders
from loader import dp, bot


class FSMDilivery(StatesGroup):
    product = State()
    name = State()
    number = State()
    volume = State()
    time = State()


@dp.callback_query_handler(Text(startswith='buy'), state=None)
async def callback_client(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer('Вы выбрали СДЕЛАТЬ ПРЕДЗАКАЗ')
    name = await get_name_item(int(callback_query.data.replace('buy', '').split(':')[1]))
    await callback_query.message.answer(
        f"Вы выбрали: {name}.\n Оформление заказа.\nЧто бы отменить заказ нажмите '/cancel'")
    async with state.proxy() as data:
        data['product'] = name
    await FSMDilivery.number.set()
    await bot.send_message(callback_query.from_user.id, 'Напиши свой номер телефона')
    # await bot.send_message(admin_id, f'Принят заказ от пользователя {callback_query.from_user.username}/номер:')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_orders(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Заказ отменен')


# @dp.message_handler(state=FSMDilivery.name)
# async def chenge_name(message: types.Message, state: FSMContext):
#     async with state.proxy() as data:
#         data['name'] = message.text
#     await FSMDilivery.next()
#     await message.reply('Теперь напиши свой номер телефона.\n(Не ошибись!)')


@dp.message_handler(state=FSMDilivery.number)
async def chenge_number(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(text=f"{i}л.") for i in range(1, 6)]
    if not re.match(r'^(\+375|80)(29|25|44|33)(\d{3})(\d{2})(\d{2})$', message.text):
        await message.reply('Не корректный номер телефона, попробуйте еще раз')
    else:
        async with state.proxy() as data:
            data['name'] = message.from_user.full_name
            data['number'] = message.text
        await FSMDilivery.next()
        await message.reply('Теперь выбери объем который тебе нужен!\n'
                            'Или введи соё количество. \n'
                            'Вводи только число литров!', reply_markup=markup.add(*buttons))


@dp.message_handler(state=FSMDilivery.volume)
async def chenge_vilume(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardRemove()
    if not re.match(r'^\d{1,2}л\.$', message.text):
        await message.reply('Ты ввел не только символы!')
    else:
        async with state.proxy() as data:
            data['volume'] = message.text

    await FSMDilivery.next()
    await message.reply('Теперь напишите время к которому вас ждать!', reply_markup=markup)


@dp.message_handler(state=FSMDilivery.time)
async def chenge_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['time'] = message.text

    # Получение данных из состояния
    state_data = await state.get_data()

    # await sql_add_orders(state)
    await sql_read_orders(message, state_data)
    await state.finish()
    await message.answer(f'Заказ сформирован.\n'
                         f'Вы выбрали:\n{state_data["product"]} ({state_data["volume"]})\n'
                         f'Заказ будет готов к {state_data["time"]}\n'
                         f'Приезжайте и забирайте свой холодненький заказ 😉!')
