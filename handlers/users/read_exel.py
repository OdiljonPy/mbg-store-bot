from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from utils.misc.assistants import send_products_xlsx, check_file_xlsx, get_user_lang

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

    await message.bot.download_file(file_path=file_path,
                                    destination=f"data/products/{message.from_user.id}_products.xlsx")
    if not await check_file_xlsx(message.from_user.id):
        await message.answer(
            text={
                'uz': "Ushbu fayl berilgan shartlarga to'g'ri kelmadi.",
                'ru': "Этот файл не соответствует указанным условиям."
            }.get(lang)
        )
        return

    result = await send_products_xlsx(message.from_user.id)
    if result.status_code == 200:
        await message.answer(
            text=f"{result.json().get('result')}"
        )
        return

    await message.answer(
        text=f"{result.json().get('error')}"
    )
