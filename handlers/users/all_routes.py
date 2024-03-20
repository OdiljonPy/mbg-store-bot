from aiogram import Router
from . import start
from . import help
from . import echo
from . import search_default
from . import search_by_type
from . import search_by_searching
from . import change_language

user_router = Router()
user_router.include_routers(
    help.router,
    start.router,
    change_language.router,
    search_by_type.router,
    search_by_searching.router,
    search_default.router,
    echo.router,
)
