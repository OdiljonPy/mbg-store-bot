import logging
import requests
from aiogram import Bot
from data.config import BACKEND_URL
from keyboards.default.main import main_button


async def notify_users_(bot: Bot):
    """ notify users when the bot is restarted. """
    users = requests.get(
        url=f"{BACKEND_URL}/get-all-users/",
    ).json().get('result')
    for user in users:
        try:
            await bot.send_message(
                chat_id=user.get('telegram_id'),
                text={
                    'uz': "Foydalanuvchilar uchun botga yangi imkoniyatlar qo'shildi 🎉.",
                    'ru': "Для пользователей в бот добавлены новые возможности 🎉."
                }.get(user.get('language')),
                reply_markup=await main_button(lang=user.get('language'))
            )

        except Exception as err:
            logging.error(msg=f"{err} User: {user}")
