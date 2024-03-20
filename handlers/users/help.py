from aiogram import types, Router
from aiogram.filters import Command
from keyboards.default.main import main_button
from utils.misc.assistants import get_user_lang, network_error_message

router = Router()


@router.message(Command('help'))
async def bot_help(message: types.Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
        return

    await message.answer(text={
        'uz': "Buyruqlar: \n"
              "/start - Botni ishga tushirish\n"
              "/help - Yordam\n"
              "Murojaat uchun: +998900969699\n"
              "@abduvaitov_o",

        'ru': "Команды: \n"
              "/start стартового бота \n"
              "/help - Помощь\n"
              "Для подачи заявки: +998900969699\n"
              "@abduvaitov_o"
    }.get(lang))
