import requests
from data.config import BACKEND_URL
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.misc.assistants import send_error_notify_

MainButtonText = {
    'uz': ["Tur bo'yicha izlash 🔍", "🏠 Asosiy sahifa", "🌎 Tilni o'zgartirish"],
    'ru': ["Поиск по типу 🔍", "🏠 Главная страница", "🌎 Изменить язык"]
}


async def main_button(lang: str):
    button = ReplyKeyboardBuilder()
    button.add(KeyboardButton(text=MainButtonText[lang][0]))
    button.add(KeyboardButton(text=MainButtonText[lang][1]))
    button.add(KeyboardButton(text=MainButtonText[lang][2]))

    button.adjust(*[1, 2])
    return button.as_markup(resize_keyboard=True)


async def language():
    button = ReplyKeyboardBuilder()
    button.add(KeyboardButton(text="🇺🇿 O'zbek")),
    button.add(KeyboardButton(text="🇷🇺 Русский"))
    button.adjust(2),
    return button.as_markup(resize_keyboard=True)


async def product_type(lang: str):
    result = requests.get(
        url=f"{BACKEND_URL}/category",
        headers={"Accept-Language": lang}
    )

    if result.status_code != 200 and not result.json().get('ok'):
        await send_error_notify_(
            status_code=result.status_code,
            line=32, filename='default/main.py',
            request_type='GET'
        )
    type_list = [name.get("name") for name in result.json().get("result")]

    button = ReplyKeyboardBuilder()
    for type_ in type_list:
        button.add(KeyboardButton(text=f"{type_}"))

    button.add(*[
        KeyboardButton(text=MainButtonText.get(lang)[1]),
        KeyboardButton(text=MainButtonText.get(lang)[2])
    ])
    if len(type_list) % 2 == 1:
        button.adjust(*[2] * int(len(type_list) / 2) + [1] + [2])
    else:
        button.adjust(*[2] * int(len(type_list) / 2) + [2])

    return button.as_markup(resize_keyboard=True)


async def create_p_name(lang: str, name: str) -> dict:
    result = requests.get(
        url=f"{BACKEND_URL}/store/products/chace_name/?q={name}",
        headers={"Accept-Language": lang}
    ).json()

    if not result.get('result'):
        return {}

    name_list = result.get("result")
    button = ReplyKeyboardBuilder()
    for text in name_list:
        button.add(KeyboardButton(text=text))

    button.add(*[
        KeyboardButton(text=MainButtonText.get(lang)[1]),
        KeyboardButton(text=MainButtonText.get(lang)[2])
    ])
    if len(name_list) % 2 == 1:
        button.adjust(*[2] * int(len(name_list) / 2) + [1] + [2])
    else:
        button.adjust(*[2] * int(len(name_list) / 2) + [2])

    return {
        'btn': button.as_markup(resize_keyboard=True),
        'list': name_list}
