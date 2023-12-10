from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from utils.misc import rate_limit


@rate_limit(5, 'help')
@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = [
        'Список команд: ',
        '/start - Сделать предзаказ\n'
        'Тут можно оформить предзаказ на холодненькое и потом приехать его забрать. 😁',
        '/help - Получить справку',
        '/generate_image - Сгенерировать изображение по запросу.',
        'Так же ты можешь задавать любые интересующие тебя вопросы боту, и он постараеться на них дать ответ!\n'
        'Но мы то знаем что тебя интересует 😉🍺',
        'Чат разработчика - https://t.me/ProDimas'
    ]
    await message.answer('\n'.join(text))
