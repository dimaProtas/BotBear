from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from keyboards.default.admin_kb import button_case_admin
from keyboards.reply.start_keyboard import start_markup
from loader import dp, bot
from utils.db_api.db_commands import pg_read, item_delete


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, f'Привет, {message.from_user.full_name}! '
                         f'Жми /menu', reply_markup=start_markup)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите боту: \n https://t.me/test_protasevich_bot',
                            reply_markup=start_markup)


@dp.message_handler(user_id=admins, commands='moderator')
async def make_change_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Что хозяин надо?', reply_markup=button_case_admin)
    await message.delete()


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def callback_run(callback_query: types.CallbackQuery):
    await item_delete(int(callback_query.data.replace('del ', '')))
    await callback_query.answer(f"Товар № {callback_query.data.replace('del ', '')} удален", show_alert=True)


@dp.message_handler(user_id=admins, commands='Удалить')
async def delete_product(message: types.Message, state: FSMContext):
    read = await pg_read()
    for i in read:
        await bot.send_message(message.from_user.id, i, reply_markup=InlineKeyboardMarkup().add(
                                   InlineKeyboardButton(f'Удалить {i}', callback_data=f'del {i.id}')))


@dp.message_handler(Text(startswith='Местоположение'))
async def bot_location(message: types.Message):
    await message.answer_photo('https://avatars.mds.yandex.net/get-altay/10702157/2a0000018b0bfc0aee7d5b6ac895a9563af3/XXXL',
                               caption='Гродненская область, Волковыск, улица Жолудева 74C')
    await bot.send_location(message.chat.id, latitude=53.154044, longitude=24.440211, horizontal_accuracy=500)
    await message.delete()


@dp.message_handler(Text(startswith='Контакты'))
async def bot_contakt(message: types.Message):
    await message.answer(f'Наши контакты:\nАдминистратор: https://t.me/weissrusslander\n'
                         f'По вопросам сотрудничества: \n+375 29 236 1002')