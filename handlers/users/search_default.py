import requests
from aiogram import types, Router
from data.config import BACKEND_URL
from keyboards.default.main import main_button
from utils.misc.assistants import get_user_lang, network_error_message, send_error_notify_

router = Router()


@router.message()
async def search_default(message: types.Message):
    lang = await get_user_lang(user_id=message.from_user.id)
    if not lang:
        await network_error_message(message=message, button=await main_button(lang='uz'))
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
            line=12, filename='search_default.py',
            request_type='POST'
        )
        return

    if response.json().get('result').get('numberOfElements') == 0:
        await message.answer(
            text={
                'uz': "Siz izlagan mahsulot topilmadi",
                'ru': "Не удалось найти продукт, который вы искали"
            }.get(lang)
        )
        return
    from aiogram.utils.markdown import hlink
    data = response.json().get("result")
    for content in data.get('content'):
        img_list = content.get("images")
        url = hlink(title="map", url=f"https://maps.google.com/maps?"
                                     f"q={content.get('store').get('latitude')},{content.get('store').get('longitude')}"
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
        return
