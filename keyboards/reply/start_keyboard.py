from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


buttons = [KeyboardButton(text='Местоположение'), KeyboardButton(text='Контакты')]
button_menu = KeyboardButton(text='/menu')
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(*buttons).add(button_menu)
