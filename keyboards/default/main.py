import requests
from data.config import BACKEND_URL
from aiogram.types import KeyboardButton, WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder

MainButtonText = {
    'uz': ["📱 Mini ilovani ochish", "🏠 Asosiy sahifa", "🌎 Tilni o'zgartirish"],
    'ru': ["📱 Открыть мини-приложение", "🏠 Главная страница", "🌎 Изменить язык"]
}


async def main_button(lang: str):
    lang_prefix = 'ru' if lang == 'ru' else 'uz'
    catalog_url = f"https://mbgstore.uz/{lang_prefix}/catalog?filters="

    button = ReplyKeyboardBuilder()
    button.add(
        KeyboardButton(
            text=MainButtonText[lang][0],
            web_app=WebAppInfo(url=catalog_url)
        )
    )
    button.add(KeyboardButton(text=MainButtonText[lang][1]))
    button.add(KeyboardButton(text=MainButtonText[lang][2]))

    button.adjust(1, 2)
    return button.as_markup(resize_keyboard=True)


async def language():
    button = ReplyKeyboardBuilder()
    button.add(KeyboardButton(text="🇺🇿 O'zbek"))
    button.add(KeyboardButton(text="🇷🇺 Русский"))
    button.adjust(2)
    return button.as_markup(resize_keyboard=True)


async def product_type(lang: str):
    lang_prefix = 'ru' if lang == 'ru' else 'uz'
    catalog_url = f"https://mbgstore.uz/{lang_prefix}/catalog?filters="

    button = ReplyKeyboardBuilder()
    button.add(
        KeyboardButton(
            text=MainButtonText.get(lang)[0],
            web_app=WebAppInfo(url=catalog_url)
        )
    )
    button.add(*[
        KeyboardButton(text=MainButtonText.get(lang)[1]),
        KeyboardButton(text=MainButtonText.get(lang)[2])
    ])
    button.adjust(1, 2)
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
        'list': name_list
    }