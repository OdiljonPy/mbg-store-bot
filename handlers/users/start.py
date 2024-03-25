import requests
from aiogram import F
from aiogram import types, Router
from states.states import LangState
from data.config import BACKEND_URL
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, language
from utils.misc.assistants import get_user_lang, send_error_notify_, network_error_message

router = Router()

answer_t = {
    'uz': "Kerakli mahsulot nomini kiriting\nyoki berilgan tugmalar orqali kerakli amalni bajaring.",
    'ru': "Введите желаемое название продукта\nили выполните желаемое действие с помощью предоставленных кнопок."
}


@router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    lang = await get_user_lang(user_id=message.from_user.id)
    if lang:
        await message.answer(
            text=answer_t.get(lang),
            reply_markup=await main_button(lang=lang)
        )
        return
    await message.answer(
        text="Assalomu alaykum\n"
             "Botga xush kelibsiz\n\n"
             "Здравствуйте\n"
             "Добро пожаловать в бот"
    )
    await message.answer(
        text="Foydalanish uchun tilni tanlang.\n"
             "Выберите язык для использования.",
        reply_markup=await language()
    )

    response = requests.post(
        url=f"{BACKEND_URL}/create/",
        json={
            "full_name": f"{message.from_user.full_name}",
            "telegram_id": message.from_user.id
        }
    )

    if response.status_code != 201:
        await send_error_notify_(
            status_code=response.status_code,
            line=40, filename='start.py',
        )
        await network_error_message(message=message)
        return

    await state.set_state(LangState.lang)


@router.message(LangState.lang, F.text.in_(["Uzb", "Rus"]))
async def user_language(message: types.Message, state: FSMContext):
    if message.text == "Uzb":
        lang = 'uz'
    else:
        lang = 'ru'

    response = requests.post(
        url=f"{BACKEND_URL}/create/",
        json={
            "full_name": f"{message.from_user.full_name}",
            "telegram_id": message.from_user.id,
            "language": lang
        }
    )
    if response.status_code != 201:
        await send_error_notify_(
            status_code=response.status_code,
            line=65, filename='start.py'
        )
        await network_error_message(message=message)
        await state.set_state(LangState.lang)
        return

    await message.answer(
        text=answer_t.get(lang),
        reply_markup=await main_button(lang=lang)
    )
    await state.clear()


@router.message(LangState.lang)
async def user_language(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(
        text="Foydalanish uchun tilni tanlang.\n"
             "Выберите язык для использования.",
        reply_markup=await language()
    )
    await state.set_state(LangState.lang)


@router.message(F.text.in_(["🏠 Asosiy sahifa", "🏠 Главная страница"]))
async def main_page(message: types.Message, state: FSMContext):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
        await state.clear()
        return

    await message.answer(
        text=answer_t.get(lang),
        reply_markup=await main_button(lang=lang)
    )
    await state.clear()
