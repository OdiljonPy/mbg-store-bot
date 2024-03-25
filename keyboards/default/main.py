import requests
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import KeyboardButton
from data.config import BACKEND_URL
from loader import bot

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


async def send_error_message(user_id: int):
    await bot.send_message(
        chat_id=user_id,
        text="Tarmoqda xatorlik yuz berdi\n"
             "Iltimos qaytadan urinib ko'ring.\n\n"
             "В сети произошла ошибка\n"
             "Пожалуйста, попробуйте еще раз."
    )


def product_type_list(user_id):
    result = requests.get(f"{BACKEND_URL}/check/?telegram_id={user_id}")

    if not result.json().get('result').get('language'):
        return []
    result = requests.get(
        url=f"{BACKEND_URL}/category/",
        headers={"Accept-Language": result.json().get('result').get('language')}
    ).json().get("result")

    return [name.get('name') for name in result]
