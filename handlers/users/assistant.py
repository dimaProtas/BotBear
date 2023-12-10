import base64
import os
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from loader import dp, bot
from utils.openai.candinski import Text2ImageAPI
from utils.openai.connect_openai import openai_send
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv

load_dotenv()


class FSMDilivery(StatesGroup):
    image = State()
    style = State()


@dp.message_handler(Command("generate_image"), state=None)
async def bot_generate_image(message: types.Message, state: FSMContext):
    await message.answer(f'{message.from_user.full_name}, напиши какое изображение ты хочешь получить!\n'
                         f'И придёться чуть-чуть подождать пока я сгенерирую тебе изображение.')
    await FSMDilivery.image.set()


@dp.message_handler(state=FSMDilivery.image)
async def change_image(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [KeyboardButton(text=f"KANDINSKY", callback_data=0), KeyboardButton(text=f"UHD", callback_data=1),
               KeyboardButton(text=f"ANIME", callback_data=2), KeyboardButton(text=f"DEFAULT", callback_data=3)]
    async with state.proxy() as data:
        data['image'] = message.text
    await FSMDilivery.next()
    await message.answer('Теперь выбери стиль изображения', reply_markup=markup.add(*buttons))


@dp.message_handler(state=FSMDilivery.style)
async def chenge_style(message: types.Message, state: FSMContext):
    markup = ReplyKeyboardRemove()
    state_data = await state.get_data()

    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', os.getenv("KANDINSKY_API_KEY"), os.getenv("KANDINSKY_SECRET_KEY"))
    model_id = api.get_model()
    uuid = api.generate(state_data['image'], model_id, style=message.text)
    images = api.check_generation(uuid)
    # print(images)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)

    with open("image.jpg", "wb") as file:
        file.write(image_data)
    # response = generate_img(message.text)
    # await message.answer(f'Вот твое изображение по запросу \n "{message.text}"')
    await message.answer_photo(open('./image.jpg', 'rb'), caption=f'Вот твое изображение по запросу \n '
                                                                  f'"{state_data["image"]}"\n'
                                                                  f'Стиль: {message.text}', reply_markup=markup)

    await state.finish()


@dp.message_handler()
async def bot_assistant(message: types.Message):
    # await message.answer(f'Привет {message.from_user.full_name}, что ты у меня хочешь спросить?')

    user_message = {"role": "user", "content": message.text}
    response = await openai_send([user_message])
    await message.answer(response, parse_mode="HTML")
