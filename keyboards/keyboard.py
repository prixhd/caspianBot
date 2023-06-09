import aiogram
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, \
    InlineKeyboardMarkup
from aiogram import types


# KEYBOARD FROM COMMAND /START
async def start_command():
    startButton = []
    startKeyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1, one_time_keyboard=True)

    startButton.append('Стать частью команды CaspianTech')
    startButton.append('Заказать работу')

    startKeyboard.add(*startButton)

    return startKeyboard


async def form_for_team_command():
    fromTeamKeyboard = InlineKeyboardMarkup()
    fromTeamKeyboard.row(InlineKeyboardButton(text="Да", callback_data="yes"))
    return fromTeamKeyboard
