from aiogram import F, Router
from contextlib import suppress
import os
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

router = Router()

WEB_APP_URL = "https://mbgstore.uz/"
ADMIN_IDS = [int(admin_id) for admin_id in os.getenv("ADMINS", "").split(",") if admin_id.strip()]
USER_LANGS = {}

class FeedbackState(StatesGroup):
    waiting_text = State()


def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🇺🇿 O‘zbekcha", callback_data="lang_uz")],
            [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        ]
    )


def main_menu_keyboard(lang: str) -> InlineKeyboardMarkup:
    texts = {
        "uz": {
            "open": "Ochish",
            "feedback": "✍️ Fikr qoldirish",
            "change_lang": "🌎 Tilni o'zgartirish",
        },
        "ru": {
            "open": "Открыть",
            "feedback": "✍️ Оставить отзыв",
            "change_lang": "🌎 Изменить язык",
        },
    }

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=texts[lang]["open"],
                    web_app=WebAppInfo(url=WEB_APP_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text=texts[lang]["feedback"],
                    callback_data=f"feedback_{lang}",
                )
            ],
            [
                InlineKeyboardButton(
                    text=texts[lang]["change_lang"],
                    callback_data="change_lang",
                )
            ],
        ]
    )


def feedback_admin_text(lang: str, user, feedback_text: str) -> str:
    username = f"@{user.username}" if user.username else "Username yo'q"

    if lang == "ru":
        return (
            "📝 Новый отзыв\n\n"
            f"👤 Имя: {user.full_name}\n"
            f"🔗 Username: {username}\n"
            f"🆔 User ID: {user.id}\n"
            "🌐 Язык: ru\n\n"
            f"💬 Отзыв:\n{feedback_text}"
        )

    return (
        "📝 Yangi otziv\n\n"
        f"👤 Ism: {user.full_name}\n"
        f"🔗 Username: {username}\n"
        f"🆔 User ID: {user.id}\n"
        "🌐 Til: uz\n\n"
        f"💬 Otziv:\n{feedback_text}"
    )


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard(),
    )


@router.message(Command("language"))
async def language_command_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard(),
    )


@router.message(F.text == "/id")
async def get_user_id_handler(message: Message):
    await message.answer(f"Sizning Telegram ID: {message.from_user.id}")


@router.callback_query(F.data == "change_lang")
async def change_language_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        text="Tilni tanlang / Выберите язык",
        reply_markup=language_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "lang_uz")
async def uz_language_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    USER_LANGS[callback.from_user.id] = "uz"
    await callback.message.edit_text(
        text="Xush kelibsiz",
        reply_markup=main_menu_keyboard("uz"),
    )
    await callback.answer()


@router.callback_query(F.data == "lang_ru")
async def ru_language_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    USER_LANGS[callback.from_user.id] = "ru"
    await callback.message.edit_text(
        text="Добро пожаловать",
        reply_markup=main_menu_keyboard("ru"),
    )
    await callback.answer()


@router.callback_query(F.data == "feedback_uz")
async def feedback_uz_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FeedbackState.waiting_text)
    await state.update_data(lang="uz")
    await callback.message.answer(text="Fikringizni yozing")
    await callback.answer()


@router.callback_query(F.data == "feedback_ru")
async def feedback_ru_handler(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FeedbackState.waiting_text)
    await state.update_data(lang="ru")
    await callback.message.answer(text="Напишите ваш отзыв")
    await callback.answer()


@router.message(StateFilter(FeedbackState.waiting_text), F.text)
async def send_feedback_to_admin_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang", "uz")

    user = message.from_user

    await state.clear()

    if lang == "ru":
        await message.answer("Спасибо за отзыв")
    else:
        await message.answer("Fikringiz uchun rahmat")

    for admin_id in ADMIN_IDS:
        if admin_id == user.id:
            continue

        admin_lang = USER_LANGS.get(admin_id, "uz")
        admin_text = feedback_admin_text(
            lang=admin_lang,
            user=user,
            feedback_text=message.text,
        )

        with suppress(Exception):
            await message.bot.send_message(
                chat_id=admin_id,
                text=admin_text,
            )


@router.message(StateFilter(None), F.text)
async def ignore_unknown_text_handler(message: Message):
    return