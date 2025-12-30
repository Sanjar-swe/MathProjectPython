from aiogram.fsm.state import State, StatesGroup

class Registration(StatesGroup):
    waiting_for_full_name = State()

class TestState(StatesGroup):
    taking_test = State()
