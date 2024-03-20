import requests
from aiogram import types, Router
from difflib import SequenceMatcher
from data.config import BACKEND_URL
from aiogram.fsm.context import FSMContext
from keyboards.default.main import main_button
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_

router = Router()


@router.message()
async def search_default(message: types.Message):
    response = requests.get(
        url=f"{BACKEND_URL}/[message.text]",
        json={}
    )

    if response.status_code != 200:
        await network_error_message(message)
        await send_error_notify_(
            status_code=response.status_code,
            line=14, filename='search_default.py',
            request_type='GET'
        )
    await message.answer(
        text=f"{message.text.title()} haqida malumotlar!"
    )
