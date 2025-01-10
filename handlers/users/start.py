import requests
from aiogram import F
from aiogram import types, Router
from states.states import LangState
from aiogram.enums import ParseMode
from data.config import BACKEND_URL
from states.states import SearchByType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, language, product_type
from utils.misc.assistants import get_user_lang, send_error_notify_, network_error_message

router = Router()

answer_t = {
    'uz': "🖋 Menga mahsulot nomini yozib yuboring yoki\n"
          "👇 Berilgan tugmalar orqali kerakli amallar ketma-ketligini bajaring.",
    'ru': "🖋 Напишите Мне название продукта или\n"
          "👇 Выполните необходимую последовательность действий по заданным кнопкам."
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
        text=f"🇺🇿  Assalomu alaykum <b>{message.from_user.full_name}</b>.\n"
             f"Botga xush kelibsiz.\n"
             f"Bu bot yordamida siz <b>MBG-Store</b> online platformasidan "
             f"kerakli mahsulotlar haqida bilib olishingiz mumkin.\n"
             f"👇 Foydalanish uchun tilni tanlang\n\n"
             f"🇷🇺  Здравствуйте <b>{message.from_user.full_name}</b>.\n"
             f"Добро пожаловать в бот.\n"
             f"С помощью этого бота вы сможете узнать о необходимых товарах онлайн-платформы <b>MBG-Store</b>.\n"
             f"👇 Выберите язык для использования",
        parse_mode=ParseMode.HTML,
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
            line=46, filename='start.py',
            request_type='POST'
        )
        await network_error_message(message=message)
        return

    await state.set_state(LangState.lang)


@router.message(LangState.lang, F.text.in_(["🇺🇿 O'zbek", "🇷🇺 Русский"]))
async def user_language(message: types.Message, state: FSMContext):
    if message.text == "🇺🇿 O'zbek":
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
            line=73, filename='start.py',
            request_type='POST'
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


@router.message(F.text.in_(["Tur bo'yicha izlash 🔍", "Поиск по типу 🔍"]))
async def search_by_type_button(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return

    await message.answer(
        text={
            'uz': "👇 Sizni qiziqtirgan mahsulot turini tanlang\n",
            'ru': "👇 Выберите интересующий вас тип продукта\n"
        }.get(lang),
        reply_markup=await product_type(lang)
    )
    await state.set_state(SearchByType.p_type)
