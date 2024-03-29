import requests
from aiogram import types
from typing import Union, Optional
from data.config import BACKEND_URL
from aiogram.utils.markdown import hlink
from aiogram.fsm.context import FSMContext
from data.config import ERROR_NOTIFY_BOT_TOKEN, ERROR_NOTIFY_CHANNEL_ID


async def send_error_notify_(status_code: int, line: int, filename: str, request_type: str = 'POST') -> None:
    message = ("MBG-Store-Bot:\n\n"
               f"Request {request_type} so'rovda xatolik yuz berdi.\n"
               f"{filename}  {line}-qator\n"
               f"request.status_code: {status_code}")

    # requests.post(
    #     url=f'https://api.telegram.org/bot{ERROR_NOTIFY_BOT_TOKEN}/sendMessage',
    #     data={'chat_id': ERROR_NOTIFY_CHANNEL_ID, 'text': message}
    # )


async def get_user_lang(message: types.Message, state: FSMContext) -> str:
    data = await state.get_data()
    if data.get('language'):
        print("State lang: ", data.get('language'))
        return data.get('language')

    response = requests.get(f"{BACKEND_URL}/check/?telegram_id={message.from_user.id}")

    if response.json().get("ok") and response.status_code == 200:
        if response.json().get('user'):
            lang = response.json().get('result').get('language')
            await state.update_data({'language': lang})
            return lang
        else:
            return ''
    else:
        await send_error_notify_(
            status_code=response.status_code,
            line=24, filename='assistants.py', request_type='GET'
        )
        await network_error_message(
            message=message
        )
        return ''


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


async def send_content(message: types.Message, data):
    for content in data.get('content'):
        img_list = content.get("images")
        loc_name = content.get('store').get('store_location_name')
        if loc_name is None:
            loc_name = content.get('store').get('brand_name')
        url = hlink(title=loc_name, url=f"https://maps.google.com/maps?"
                                        f"q={content.get('store').get('latitude')},"
                                        f"{content.get('store').get('longitude')}"
                    )
        media = [
            types.InputMediaPhoto(
                media=img_list.pop().get('image'),
                caption=f"Store name: {content.get('store').get('brand_name')}\n\n"
                        f"Product name: {content.get('name')}\n"
                        f"Price: {content.get('discount_price')}\n"
                        f"Discount: {content.get('discount')}%\n"
                        f"Rating: {content.get('rating')}\n"
                        f"Description: {content.get('description')}\n\n"
                        f"Location: {url}"
            )]

        media += list(map(lambda img: types.InputMediaPhoto(media=img.get('image')), img_list))

        await message.answer_media_group(
            media=media
        )
