import requests
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from data.config import BACKEND_URL

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
    # type_list = requests.get(
    #     url=f"{BACKEND_URL}/"
    # )
    # default type
    type_list = ["Mevalar", "Ro'zg'or buyumlari", "Kiyimlar", "Qurilish", "Jihozlar"]
    button = ReplyKeyboardBuilder()
    for type_ in type_list:
        button.add(KeyboardButton(text=f"{type_}"))

    button.add(*[
        KeyboardButton(text=MainButtonText.get('uz')[1]),
        KeyboardButton(text=MainButtonText.get('uz')[2])
    ])
    if len(type_list) % 2 == 1:
        button.adjust(*[2] * int(len(type_list) / 2) + [1] + [2])
    else:
        button.adjust(*[2] * int(len(type_list) / 2) + [2])

    return button.as_markup(resize_keyboard=True)


def product_type_list():
    # return type list
    # return requests.get(
    #     url=f"{BACKEND_URL}/"
    # )

    return ["Mevalar", "Ro'zg'or buyumlari", "Kiyimlar", "Qurilish", "Jihozlar"]
