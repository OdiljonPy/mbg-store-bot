import os
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button
from utils.misc.assistants import (
    send_products_xlsx, check_file_baseProduct_xlsx,
    get_user_lang, check_file_Product_xlsx
)

router = Router()


@router.message(F.content_type == 'document')
async def download_file(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return
    file_id = message.document.file_id
    file = await message.bot.get_file(file_id)
    file_path = file.file_path
    if not file_path.endswith('.xlsx'):
        await message.answer(
            text={
                'uz': "Ushbu fayl «exel» emas.",
                'ru': "Этот файл не «exel»."
            }.get(lang)
        )
        return
    await message.bot.download_file(
        file_path=file_path, destination=f"data/products/{message.from_user.id}_products.xlsx")

    btn = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text='Product'),
                types.KeyboardButton(text='BaseProduct'),
            ]
        ], resize_keyboard=True)

    await message.answer(
        text={
            'uz': "Malumot turini tanlang!",
            'ru': "Выберите тип данных!"
        }.get(lang),
        reply_markup=btn
    )


@router.message(F.text.in_(['Product', 'BaseProduct']))
async def create_product(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
        return

    if message.text == 'Product':
        check_res = await check_file_Product_xlsx(message.from_user.id)
    else:
        check_res = await check_file_baseProduct_xlsx(message.from_user.id)

    product_type = {'Product': 'product', 'BaseProduct': 'base_product'}.get(message.text)

    if not check_res:
        await message.answer(
            text={
                'uz': "Ushbu fayl berilgan shartlarga to'g'ri kelmadi.",
                'ru': "Этот файл не соответствует указанным условиям."
            }.get(lang),
            reply_markup=await main_button(lang)
        )
        os.remove(f'data/products/{message.from_user.id}_products.xlsx')
        return

    await message.answer(
        text={
            'uz': "Malumotlar yuklanmoqda",
            'ru': "Загрузка данных"
        }.get(lang),
        reply_markup=await main_button(lang)
    )

    result = await send_products_xlsx(message.from_user.id, type_=product_type)
    os.remove(f'data/products/{message.from_user.id}_products.xlsx')
    if result.status_code == 200:
        await message.answer(
            text=f"{result.json().get('result')}",
            reply_markup=await main_button(lang)
        )
        return

    await message.answer(
        text=f"{result.json().get('error')}"
    )
