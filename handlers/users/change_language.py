import requests
from data.config import BACKEND_URL
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, product_type_list, product_type, language
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_
from states.states import ChangeLang

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

    response = requests.get(
        url=f"{BACKEND_URL}/[change - lang]"
    )

    if response.status_code != 200:
        await network_error_message(message=message, button=await main_button(lang))
        await state.clear()
        return

    await message.answer(
        text={
            'ru': "Til muvaffaqiyatli o'zgartirildi!",
            'uz': "Язык успешно изменен!"
        }.get(lang),
        reply_markup=await main_button(lang)
    )
