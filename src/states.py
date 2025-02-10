from aiogram.fsm.state import State, StatesGroup


class SetCardStateGroup(StatesGroup):
    wait_card = State()


class GetHistoryStateGroup(StatesGroup):
    choose_period = State()
