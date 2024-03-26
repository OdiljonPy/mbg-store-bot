import requests
from data.config import BACKEND_URL
from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

MainButtonText = {
    'uz': ["Qidiruv 🔍", "🏠 Asosiy sahifa", "🔄 Til"],
    'ru': ["Поиск 🔍", "🏠 Главная страница", "🔄 Язык"]
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
    button.add(KeyboardButton(text="Uzb")),
    button.add(KeyboardButton(text="Rus"))
    button.adjust(2),
    return button.as_markup(resize_keyboard=True)


async def product_type(lang: str):
    result = requests.get(
        url=f"{BACKEND_URL}/category",
        headers={"Accept-Language": lang}
    ).json().get("result")
    type_list = [name.get("name") for name in result]

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


def product_type_list(user_id) -> list:
    result = requests.get(f"{BACKEND_URL}/check/?telegram_id={user_id}")

    if not result.json().get('result').get('language'):
        return []
    result = requests.get(
        url=f"{BACKEND_URL}/category/",
        headers={"Accept-Language": result.json().get('result').get('language')}
    ).json().get("result")

    return [name.get('name') for name in result]


def get_category_id(category: str, user_id: int) -> int:
    result = requests.get(f"{BACKEND_URL}/check/?telegram_id={user_id}")

    if not result.json().get('result').get('language'):
        return 0
    result = requests.get(
        url=f"{BACKEND_URL}/category/",
        headers={"Accept-Language": result.json().get('result').get('language')}
    ).json().get("result")

    return [name.get('id') for name in result if name.get('name') == category][0]
