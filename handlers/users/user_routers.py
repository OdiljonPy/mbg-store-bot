from aiogram import Router
from . import start
from . import help
from . import echo

user_router = Router()
user_router.include_routers(
    help.router,
    start.router,
    echo.router,
)
