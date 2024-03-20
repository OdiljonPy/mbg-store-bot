from loader import bot
from data.config import ADMINS
from aiogram import types, Router
from filters.is_admin import IsAdmin
from aiogram.filters import CommandStart
from notify.notify_handlers.channel_notify import new_user_addition_notification

router = Router()


@router.message(CommandStart(), IsAdmin(user_ids=list(map(int, ADMINS))))
async def bot_start(message: types.Message):
    await message.answer(
        text="Xush kelibsiz Super Admin!"
    )


@router.message(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!"
                         f"\nBotga xush kelibsiz!",
                         )
    await new_user_addition_notification(
        about_user=f"Yangi foydalanuvchi!"
                   f"\nIsm: {message.from_user.full_name}"
                   f"\nUsername: @{message.from_user.username}"
                   f"\nID: {message.from_user.id}",
        bot=bot
    )
