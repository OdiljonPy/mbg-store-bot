import requests
from aiogram import types, Router
from data.config import BACKEND_URL
from aiogram.enums import ParseMode
from states.states import SearchByName
from aiogram.fsm.context import FSMContext
from keyboards.default.main import create_p_name
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_, send_content

router = Router()


@router.message(SearchByName.name)
async def search_default_with_btn(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return
    data = await state.get_data()
    if message.text not in data.get('list'):
        await message.answer(
            text={
                'uz': "Iltimos sizga tavsiya qilingan mahsulot nomlaridan birini tanlang.\n"
                      "👇 Qidiruvni tugatish uchun <b>*🏠 Asosiy sahifa*</b> tugmasini bosing.",
                'ru': "Пожалуйста, выберите одно из рекомендуемых названий продуктов.\n"
                      "👇 Нажмите кнопку <b>*🏠 Главная страница*</b>, чтобы завершить поиск."
            }.get(lang),
            parse_mode=ParseMode.HTML
        )
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
            line=31, filename='search_default.py',
            request_type='POST'
        )
        return

    if response.json().get('result').get('numberOfElements') == 0:
        await message.answer(
            text={
                'uz': "Siz izlagan mahsulot topilmadi 😔.",
                'ru': "Не удалось найти продукт, который вы искали 😔."
            }.get(lang)
        )
        return
    await send_content(message=message, data=response.json().get("result"), lang=lang)


@router.message()
async def search_default(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return
    button = await create_p_name(lang=lang, name=message.text)

    if not button.get('list'):
        await message.answer(
            text={
                'uz': "Siz izlagan mahsulot topilmadi 😔.",
                'ru': "Не удалось найти продукт, который вы искали 😔."
            }.get(lang)
        )
        return

    await message.answer(
        text={'uz': "🎯 Mahsulot nomini tavsiyalar orasidan aniqroq tanlashingiz mumkin.\n"
                    "👇 Tavsiyalar.",
              'ru': "🎯 Вы можете более точно выбрать название продукта из рекомендаций.\n"
                    "👇 Рекомендации."}.get(lang),
        reply_markup=button.get('btn')
    )
    await state.update_data({'list': button.get('list')})
    await state.set_state(SearchByName.name)
