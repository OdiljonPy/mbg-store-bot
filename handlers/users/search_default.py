import requests
from aiogram import types, Router
from data.config import BACKEND_URL
from aiogram.fsm.context import FSMContext
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_, send_content

router = Router()


@router.message()
async def search_default(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return
    response = requests.post(
        url=f"{BACKEND_URL}/store/products/filter/",
        json={
            "q": message.text
        },
        headers={"Accept-Language": lang}
    )

    if response.status_code != 200:
        await network_error_message(message)
        await send_error_notify_(
            status_code=response.status_code,
            line=16, filename='search_default.py',
            request_type='POST'
        )
        return

    if response.json().get('result').get('numberOfElements') == 0:
        await message.answer(
            text={
                'uz': "Siz izlagan mahsulot topilmadi",
                'ru': "Не удалось найти продукт, который вы искали"
            }.get(lang)
        )
        return
    await send_content(message=message, data=response.json().get("result"))
