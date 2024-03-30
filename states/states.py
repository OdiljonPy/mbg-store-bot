from aiogram.fsm.state import State, StatesGroup


class LangState(StatesGroup):
    lang = State()


class ChangeLang(StatesGroup):
    lang = State()


class SearchByType(StatesGroup):
    p_type = State()
