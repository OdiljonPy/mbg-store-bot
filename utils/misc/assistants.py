import requests
from aiogram import types
from typing import Union, Optional
from data.config import BACKEND_URL
from data.config import ERROR_NOTIFY_BOT_TOKEN, ERROR_NOTIFY_CHANNEL_ID


async def send_error_notify_(status_code: int, line: int, filename: str, request_type: str = 'POST') -> None:
    message = ("Stadium-Finder-Bot:\n\n"
               f"Request {request_type} so'rovda xatolik yuz berdi.\n"
               f"{filename}  {line}-qator\n"
               f"request.status_code: {status_code}")

    # requests.post(
    #     url=f'https://api.telegram.org/bot{ERROR_NOTIFY_BOT_TOKEN}/sendMessage',
    #     data={'chat_id': ERROR_NOTIFY_CHANNEL_ID, 'text': message}
    # )


async def get_user_lang(user_id: int) -> str:
    # response = requests.get(f"{BACKEND_URL}/")
    #
    # if response.json().get("ok") and response.status_code == 200:
    #     return response.json().get('result').get('language')
    # else:
    #     return ''

    return 'uz'


async def network_error_message(
        message: types.Message,
        button: Optional[
            Union[
                types.InlineKeyboardMarkup, types.ReplyKeyboardMarkup, types.ReplyKeyboardRemove
            ]
        ] = None
):
    if button is None:
        await message.answer(
            text="Tarmoqda xatorlik yuz berdi\n"
                 "Iltimos qaytadan urinib ko'ring.\n\n"
                 "В сети произошла ошибка\n"
                 "Пожалуйста, попробуйте еще раз."
        )
    else:
        await message.answer(
            text="Tarmoqda xatorlik yuz berdi\n"
                 "Iltimos qaytadan urinib ko'ring.\n\n"
                 "В сети произошла ошибка\n"
                 "Пожалуйста, попробуйте еще раз.",
            reply_markup=button
        )
