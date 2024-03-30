import logging
import requests
from aiogram import Bot
from data.config import BACKEND_URL
from keyboards.default.main import main_button


async def notify_users_(bot: Bot):
    """ notify users when the bot is restarted. """
    users = requests.get(
        url=f"{BACKEND_URL}/users",
    )
    users = [
        {'id': 533774959, 'lang': 'uz'},
        {'id': 5337749599, 'lang': 'ru'},
        {'id': 5337749599, 'lang': 'uz'}
    ]

    for user in users:
        try:
            await bot.send_message(
                chat_id=user.get('id'),
                text={
                    'uz': "Foydalanuvchilar uchun botga yangi imkoniyatlar qo'shildi 🎉.",
                    'ru': "Для пользователей в бот добавлены новые возможности 🎉."
                }.get(user.get('lang')),
                reply_markup=await main_button(lang=user.get('lang'))
            )

        except Exception as err:
            logging.error(msg=f"{err} User: {user}")
