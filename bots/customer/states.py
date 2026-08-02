from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):

    waiting_password = State()