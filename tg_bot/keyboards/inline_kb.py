from aiogram import types

base_menu = types.InlineKeyboardMarkup(row_width=3)
base_menu_buttons = [
    types.InlineKeyboardButton('Начать', callback_data='start'),
    types.InlineKeyboardButton('участники', callback_data='members'),
    types.InlineKeyboardButton('доклады', callback_data='reports'),
]
base_menu.add(*base_menu_buttons)

hearer_main_menu = types.InlineKeyboardMarkup(row_width=1)
hearer_menu_buttons = [
    types.InlineKeyboardButton('заполнить анкету', callback_data='form'),
    types.InlineKeyboardButton('задать вопрос', callback_data='question'),
    types.InlineKeyboardButton('сделать донат', callback_data='donate'),
]
hearer_main_menu.add(*hearer_menu_buttons)

reporter_main_menu = types.InlineKeyboardMarkup(row_width=1)
reporter_menu_buttons = [
    types.InlineKeyboardButton('список вопросов', callback_data='queries'),
]
reporter_main_menu.add(*reporter_menu_buttons)
