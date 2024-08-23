from telebot.handler_backends import State, StatesGroup


class MyState(StatesGroup):
    state_start = State()
    state_name = State()
    state_budget = State()
    state_rating = State()
    state_history= State()