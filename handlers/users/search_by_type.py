import requests
from data.config import BACKEND_URL
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button, product_type_list, product_type
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_

router = Router()


@router.message(F.text.in_(product_type_list()))
async def search_by_type(message: types.Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
        return

    response = requests.get(
        url=f"{BACKEND_URL}/[type]",
        headers={"Accept-Language": lang}
    )
    if response.status_code != 200:
        await send_error_notify_(
            status_code=response.status_code,
            line=13, filename='search_by_type.py'
        )
        await network_error_message(message=message, button=await product_type(lang=lang))
        return

    await message.answer(
        text={
            'uz': "Berilgan type bo'yicha natijalar",
            'ru': "Результаты по данному типу"
        }.get(lang)
    )
