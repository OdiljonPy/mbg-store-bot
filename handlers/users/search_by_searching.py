from aiogram import types, Router, F
from keyboards.default.main import main_button, product_type
from utils.misc.assistants import get_user_lang, network_error_message

router = Router()


@router.message(F.text.in_(["Qidiruv 🔍", "Поиск 🔍"]))
async def search_by_type_button(message: types.Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
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
