from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

do_you_want_continue = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Да"), KeyboardButton(text = "Нет")]])

continue_using = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = "Продолжить работу")]])