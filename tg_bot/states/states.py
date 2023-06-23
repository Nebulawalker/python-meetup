from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    report = State()


class SurveyState(StatesGroup):
    birthdate = State()
    first_name = State()
    last_name = State()
    specialization = State()
    stack = State()
    hobby = State()
    goal = State()
    region = State()
