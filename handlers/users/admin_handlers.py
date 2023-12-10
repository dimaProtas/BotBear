from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import admins
from loader import dp, bot
from states.states import NewItem, Mailing
from utils.db_api.models import Item


@dp.message_handler(user_id=admins, commands=["cancel"], state=NewItem)
async def cancel(message: types.Message, state: FSMContext):
    await message.answer("Вы отменили создание товара")
    await state.reset_state()


@dp.message_handler(user_id=admins, commands=["add_item"])
async def add_item(message: types.Message):
    await message.answer("Введите название товара или нажмите /cancel")
    await NewItem.Name.set()


@dp.message_handler(user_id=admins, state=NewItem.Name)
async def enter_name(message: types.Message, state: FSMContext):
    name = message.text
    item = Item()
    item.name = name

    await message.answer(("Название: {name}"
                           "\nВведите категорию товара или нажмите /cancel").format(name=name))

    await NewItem.Category.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Category)
async def enter_name(message: types.Message, state: FSMContext):
    category = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.category_code = category
    item.category_name = category

    await message.answer(("\nКатегория: {category}"
                          "\nВведите подкатегорию товара или нажмите /cancel").format(category=category))

    await NewItem.Subcategory.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Subcategory)
async def enter_name(message: types.Message, state: FSMContext):
    subcategory = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.subcategory_code = subcategory
    item.subcategory_name = subcategory

    await message.answer(("\nПодкатегория: {subcategory}"
                           "\nВведите описание товара /cancel").format(subcategory=subcategory))

    await NewItem.Description.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Description)
async def enter_name(message: types.Message, state: FSMContext):
    description = message.text
    data = await state.get_data()
    item: Item = data.get("item")
    item.description = description
    item.description = description

    await message.answer(("\nПодкатегория: {description}"
                           "\nПришлите мне фотографию товара (не документ) или нажмите /cancel").format(description=description))

    await NewItem.Photo.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Photo, content_types=types.ContentType.PHOTO)
async def add_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    data = await state.get_data()
    item: Item = data.get("item")
    item.photo = photo

    await message.answer_photo(
        photo=photo,
        caption=("Название: {name}"
                  "\nПришлите мне цену товара в рублях или нажмите /cancel").format(name=item.name))

    await NewItem.Price.set()
    await state.update_data(item=item)


@dp.message_handler(user_id=admins, state=NewItem.Price)
async def enter_price(message: types.Message, state: FSMContext):
    data = await state.get_data()
    item: Item = data.get("item")
    try:
        price = int(message.text)
    except ValueError:
        await message.answer(("Неверное значение, введите число"))
        return

    item.price = price
    markup = InlineKeyboardMarkup(
        inline_keyboard=
        [
            [InlineKeyboardButton(text="Да", callback_data="confirm")],
            [InlineKeyboardButton(text="Ввести заново", callback_data="change")],
        ]
    )
    await message.answer(("Цена: {price:,}\n"
                           "Подтверждаете? Нажмите /cancel чтобы отменить").format(price=price),
                         reply_markup=markup)
    await state.update_data(item=item)
    await NewItem.Confirm.set()


@dp.callback_query_handler(user_id=admins, text_contains="change", state=NewItem.Confirm)
async def enter_price(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Введите заново цену товара в копейках")
    await NewItem.Price.set()


@dp.callback_query_handler(user_id=admins, text_contains="confirm", state=NewItem.Confirm)
async def enter_price(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_reply_markup()
    data = await state.get_data()
    item: Item = data.get("item")
    await item.create()
    await call.message.answer("Товар удачно создан.")
    await state.reset_state()


# Фича для рассылки по юзерам (учитывая их язык)
# @dp.message_handler(user_id=admins, commands=["tell_everyone"])
# async def mailing(message: types.Message):
#     await message.answer("Пришлите текст рассылки")
#     await Mailing.Text.set()
#
#
# @dp.message_handler(user_id=admins, state=Mailing.Text)
# async def mailing(message: types.Message, state: FSMContext):
#     text = message.text
#     await state.update_data(text=text)
#     markup = InlineKeyboardMarkup(
#         inline_keyboard=
#         [
#             [InlineKeyboardButton(text="Русский", callback_data="ru")],
#             # [InlineKeyboardButton(text="English", callback_data="en")],
#             # [InlineKeyboardButton(text="Україньска", callback_data="uk")],
#         ]
#     )
#     await message.answer(("Пользователям на каком языке разослать это сообщение?\n\n"
#                            "Текст:\n"
#                            "{text}").format(text=text),
#                          reply_markup=markup)
#     await Mailing.Language.set()
#
#
# @dp.callback_query_handler(user_id=admins, state=Mailing.Language)
# async def mailing_start(call: types.CallbackQuery, state: FSMContext):
#     data = await state.get_data()
#     text = data.get("text")
#     await state.reset_state()
#     await call.message.edit_reply_markup()
#
#     users = await User.query.where(User.language == call.data).gino.all()
#     for user in users:
#         try:
#             await bot.send_message(chat_id=user.user_id,
#                                    text=text)
#             await sleep(0.3)
#         except Exception:
#             pass
#     await call.message.answer("Рассылка выполнена.")
