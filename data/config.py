from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
CHANNEL_ID = env.str("CHANNEL_ID")
BACKEND_URL = env.str("BACKEND_URL")
ERROR_NOTIFY_CHANNEL_ID = env.str("ERROR_NOTIFY_CHANNEL_ID")
ERROR_NOTIFY_BOT_TOKEN = env.str("ERROR_NOTIFY_BOT_TOKEN")
