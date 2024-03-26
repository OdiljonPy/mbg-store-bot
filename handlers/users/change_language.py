import requests
from data.config import BACKEND_URL
from aiogram import types, Router, F
from states.states import ChangeLang
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, language
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_

router = Router()


@router.message(F.text.in_(["🔄 Til", "🔄 Язык"]))
async def change_language(message: types.Message, state: FSMContext):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
        return
    await message.answer(
        text={
            'uz': "Kerakli tilni tanlang.",
            'ru': "Выберите нужный язык."
        }.get(lang),
        reply_markup=await language()
    )
    await state.update_data({'lang': lang})
    await state.set_state(ChangeLang.lang)


@router.message(ChangeLang.lang, F.text.in_(["Uzb", "Rus"]))
async def change_language(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')

    if (message.text == 'Uzb' and lang == 'uz') or (message.text == 'Rus' and lang == 'ru'):
        await message.answer(
            text={
                'uz': "Til muvaffaqiyatli o'zgartirildi!",
                'ru': "Язык успешно изменен!"
            }.get(lang),
            reply_markup=await main_button(lang)
        )
        await state.clear()
        return

    if message.text == "Uzb":
        lang = 'uz'
    else:
        lang = 'ru'

    response = requests.post(
        url=f"{BACKEND_URL}/create/",
        json={
            "full_name": message.from_user.full_name,
            "language": lang,
            "telegram_id": message.from_user.id
        }
    )

    if response.status_code != 201:
        await network_error_message(message=message, button=await main_button(lang))
        await send_error_notify_(
            status_code=response.status_code,
            line=34, filename='change_language.py',
            request_type='POST'
        )
        await state.clear()
        return

    await message.answer(
        text={
            'uz': "Til muvaffaqiyatli o'zgartirildi!",
            'ru': "Язык успешно изменен!"
        }.get(lang),
        reply_markup=await main_button(lang)
    )
    await state.clear()


@router.message(ChangeLang.lang)
async def change_language_error(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get('lang')
    await message.answer(
        text={
            'uz': "O'zgartirish uchun tilni tanlang.\n",
            'ru': "Выберите язык для изменения."
        }.get(lang)
    )
