from data.config import CHANNEL_ID


async def check(chat_member):
    return chat_member['status'] == 'administrator' or chat_member['status'] == 'creator'


async def new_user_addition_notification(about_user, bot):
    await bot.send_message(text="Bot ishga tushdi.", chat_id=CHANNEL_ID)
    await bot.send_message(text=about_user, chat_id=CHANNEL_ID)


async def bot_launch_notification(bot):
    await bot.send_message(text="Bot ishga tushdi.", chat_id=CHANNEL_ID)
