import requests
from aiogram import types, Router
from data.config import BACKEND_URL
from aiogram.fsm.context import FSMContext
from keyboards.default.main import product_type_list, product_type
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_, send_content

router = Router()


@router.message(lambda message: message.text in product_type_list(message.from_user.id))
async def search_by_type(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return

    response = requests.get(
        url=f"{BACKEND_URL}/category/",
        headers={"Accept-Language": lang}
    )

    if response.status_code != 200 and not response.json().get('ok'):
        await network_error_message(message=message)
        await send_error_notify_(
            status_code=response.status_code,
            line=17, filename='search_by_type.py',
            request_type='GET'
        )
        return

    category_id = [name.get('id') for name in response.json().get('result') if name.get('name') == message.text][0]

    response = requests.post(
        url=f"{BACKEND_URL}/store/products/filter/",
        json={"category": category_id},
        headers={"Accept-Language": lang}
    )

    if response.status_code != 200:
        await network_error_message(message=message, button=await product_type(lang=lang))
        await send_error_notify_(
            status_code=response.status_code,
            line=33, filename='search_by_type.py',
            request_type='POST'
        )
        return
    if response.json().get('result').get('numberOfElements') == 0:
        await message.answer(
            text={
                'uz': "Tanlangan tur bo'yicha mahsulotlar topilmadi.",
                'ru': "Продукты по выбранному типу не найдены."
            }.get(lang)
        )
        return

    text = {
        'uz': "Berilgan type bo'yicha natijalar",
        'ru': "Результаты по данному типу"
    }.get(lang)
    await message.answer(
        text=text
    )

    await send_content(message=message, data=response.json().get("result"))
