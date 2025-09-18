from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from server import server

import application.keyboards as keyboards

router = Router()

class Input(StatesGroup):
    get_urls_archive_screenshots = State()
    continue_work = State()
    user_comeback = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Input.get_urls_archive_screenshots)
    await message.answer("""Привет! Данный бот работает с сайтом Web Archive, 
    который занимается сохранением изменеий на всех веб сайтах. 
    ArchiveWebSitesBot упрошает поиск архивных данных собирая их в одно сообщение.
    Пользователю достаточно лишь перейти по необходимой ссылке""")
    await message.answer("""Введи сайт, архивные данные которого хотите получить.""")

@router.message(Input.get_urls_archive_screenshots)
async def get_url(message: Message, state: FSMContext):
    await state.set_state(Input.continue_work)
    save_sites_matrix = server.get_list_available_snapshots(message.text)
    for save_sites in save_sites_matrix:
        await message.answer(' '.join(save_sites))
    await message.answer("Хочешь проверить другой сайт?", reply_markup=keyboards.do_you_want_continue)

@router.message(Input.continue_work)
async def continue_work(message: Message, state: FSMContext):
    if message.text == "Да":
        await state.set_state(Input.get_urls_archive_screenshots)
        await message.answer("Введи сайт, архивные данные которого хотите получить.")
    elif message.text == "Нет":
        await state.set_state(Input.user_comeback)
        await message.answer("Тогда до встречи!", reply_markup=keyboards.continue_using)

@router.message(Input.user_comeback)
async def user_comeback(message: Message, state: FSMContext):
    await state.set_state(Input.get_urls_archive_screenshots)
    await message.answer("Хорошо что вы вернулись. Архивные записи какого сайта вас интересуют на этот раз?")
