from telebot.handler_backends import State, StatesGroup


class MyState(StatesGroup):
    state_start = State()
    state_name = State()
    state_budget_low = State()
    state_budget_hight = State()
    state_rating = State()