from aiogram import Router
from . import start
from . import help
from . import echo
from . import search_default
from . import search_by_type
from . import change_language
from . import read_exel

user_router = Router()
user_router.include_routers(
    start.router,
    help.router,
    read_exel.router,
    change_language.router,
    search_by_type.router,
    search_default.router,
    echo.router,
)

