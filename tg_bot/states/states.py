from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    report = State()
    survey = State()



class SurveyState(StatesGroup):
    birthdate = State()
    first_name = State()
    last_name = State()
    specialization = State()
    stack = State()
    hobby = State()
    goal = State()
    region = State()

class MessageState(StatesGroup):
    question = State()
    answer = State()
    standby = State()
