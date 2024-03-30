import requests
from aiogram import F
from aiogram import types, Router
from states.states import LangState
from data.config import BACKEND_URL
from states.states import SearchByType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, language, product_type
from utils.misc.assistants import get_user_lang, send_error_notify_, network_error_message

router = Router()

answer_t = {
    'uz': "Menga mahsulot nomini yuboring\n"
          "yoki berilgan tugmalar orqali kerakli amallar ketma-ketligini bajaring.",
    'ru': "Пришлите мне название продукта\n"
          "или выполните необходимую последовательность действий с помощью предоставленных кнопок."
}


@router.message(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if lang:
        await message.answer(
            text=answer_t.get(lang),
            reply_markup=await main_button(lang=lang)
        )
        return
    await message.answer(
        text="Assalomu alaykum botga xush kelibsiz\n"
             "Menga qanday tilda murojat qilishni hohlaysiz ?\n\n"
             "Здравствуйте, добро пожаловать в бот\n"
             "На каком языке вы хотите со мной связаться ?",
        reply_markup=await language()
    )
    # await message.answer(
    #     text="Foydalanish uchun tilni tanlang.\n"
    #          "Выберите язык для использования.",
    #     reply_markup=await language()
    # )

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
            line=66, filename='start.py'
        )
        await network_error_message(message=message)
        await state.set_state(LangState.lang)
        return

    await message.answer(
        text=answer_t.get(lang),
        reply_markup=await main_button(lang=lang)
    )
    await state.set_state(None)


@router.message(LangState.lang)
async def user_language(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer(
        text="Murojat uchun tilni tanlang 🪄.\n\n"
             "Выберите язык для апелляции 🪄.",
        reply_markup=await language()
    )
    await state.set_state(LangState.lang)


@router.message(F.text.in_(["🏠 Asosiy sahifa", "🏠 Главная страница"]))
async def main_page(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    await state.set_state(None)
    if not lang:
        return

    await message.answer(
        text=answer_t.get(lang),
        reply_markup=await main_button(lang=lang)
    )


@router.message(F.text.in_(["Qidiruv 🔍", "Поиск 🔍"]))
async def search_by_type_button(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return

    await message.answer(
        text={
            'uz': "Sizni qiziqtirgan mahsulot turini tanlang\n"
                  "va turdagi mahsulotlar haqida ko'proq malumot olishingiz mumkin.",
            'ru': "Выберите интересующий вас тип продукта\n"
                  "и вы можете узнать больше о типах продуктов."
        }.get(lang),
        reply_markup=await product_type(lang)
    )
    await state.set_state(SearchByType.p_type)
