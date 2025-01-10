from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.misc.assistants import get_user_lang

router = Router()


@router.message(Command('help'))
async def bot_help(message: types.Message, state: FSMContext):
    lang = await get_user_lang(message=message, state=state)
    if not lang:
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
