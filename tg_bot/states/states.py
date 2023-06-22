from aiogram.dispatcher.filters.state import StatesGroup, State

class UserState(StatesGroup):
    report = State()


class SurveyState(StatesGroup):
    birthdate = State()
    specialization = State()
    stack = State()
    hobby = State()
    goal = State()
    region = State()