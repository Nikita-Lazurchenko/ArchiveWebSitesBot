from aiogram import Router, types
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from server import server

import application.keyboards as keyboards

router = Router()

class UserStates(StatesGroup):
    method_of_receipt = State()
    entering_url_for_message = State()
    entering_url_for_file = State()
    continue_work = State()
    user_comeback = State()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.method_of_receipt)
    await message.answer("""Привет! Данный бот работает с сайтом Web Archive, 
    который занимается сохранением и отображением изменеий на всех веб сайтах. 
    ArchiveWebSitesBot работая с API данного сайта помогает пользователю значительно упростить поиск 
    интересующих изменений.""")
    await message.answer("Введите способ получения архивных данных.", reply_markup=keyboards.method_of_receipt)

@router.message(UserStates.method_of_receipt)
async def method_of_receipt(message: Message, state: FSMContext):
    if message.text == "Файл":
        await state.set_state(UserStates.entering_url_for_file)
    elif message.text == "Сообщение":
        await state.set_state(UserStates.entering_url_for_message)
    await message.answer("Введите ссылку на сайт архивные записи которого хотите получить")

@router.message(UserStates.entering_url_for_file)
async def get_available_snapshots_file_format(message: types.Message, state: FSMContext):
    await state.set_state(UserStates.continue_work)
    file_path = server.get_file_available_snapshots(message.text)
    await message.reply_document(
        document=types.FSInputFile(
            path = file_path
        )
    )
    await message.answer("Хочешь проверить другой сайт?", reply_markup=keyboards.do_you_want_continue)

@router.message(UserStates.entering_url_for_message)
async def get_available_snapshots_message_format(message: Message, state: FSMContext):
    await state.set_state(UserStates.continue_work)
    save_sites_matrix = server.get_dates_matrix_by_year(message.text)
    for save_sites in save_sites_matrix:
        await message.answer(' '.join(save_sites))
    await message.answer("Хочешь проверить другой сайт?", reply_markup=keyboards.do_you_want_continue)

@router.message(UserStates.continue_work)
async def continue_work(message: Message, state: FSMContext):
    if message.text == "Да":
        await state.set_state(UserStates.method_of_receipt)
        await message.answer("Введите способ получения архивных данных.", reply_markup=keyboards.method_of_receipt)
    elif message.text == "Нет":
        await state.set_state(UserStates.user_comeback)
        await message.answer("Тогда до встречи!", reply_markup=keyboards.continue_using)

@router.message(UserStates.user_comeback)
async def user_comeback(message: Message, state: FSMContext):
    await message.answer("Введите способ получения архивных данных.", reply_markup=keyboards.method_of_receipt)
    await message.answer("Хорошо что вы вернулись. В каком формате выводить информацию?")
