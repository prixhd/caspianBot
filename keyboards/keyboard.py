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


async def changes_command():
    changesKeyboard = InlineKeyboardMarkup()
    changesKeyboard.row(InlineKeyboardButton(text="Да", callback_data="yes_changes")).row(InlineKeyboardButton(text="Нет", callback_data="no_changes"))
    return changesKeyboard


async def form_for_team_unsuccess_command():
    formTeamUnsuccessKeyboard = InlineKeyboardMarkup()

    formTeamUnsuccessKeyboard.row(InlineKeyboardButton(text='1', callback_data="first_question_form"),
                                  InlineKeyboardButton(text='2', callback_data="second_question_form"),
                                  InlineKeyboardButton(text='3', callback_data="third_question_form"))

    return formTeamUnsuccessKeyboard


async def order_work_unsuccess_command():
    orderWorkUnsuccessKeyboard = InlineKeyboardMarkup()

    var = orderWorkUnsuccessKeyboard.row(InlineKeyboardButton(text='1', callback_data="1_q_order"),
                                         InlineKeyboardButton(text='2', callback_data="2_q_order")) \
        .row(InlineKeyboardButton(text='3', callback_data="3_q_order"),
             InlineKeyboardButton(text='4', callback_data="4_q_order")) \
        .row(InlineKeyboardButton(text='5', callback_data="5_q_order"),
             InlineKeyboardButton(text='6', callback_data="6_q_order")) \
        .row(InlineKeyboardButton(text='7', callback_data="7_q_order"),
             InlineKeyboardButton(text='8', callback_data="8_q_order")) \
        .row(InlineKeyboardButton(text='9', callback_data="9_q_order"),
             InlineKeyboardButton(text='10', callback_data="10_q_order")) \
        .row(InlineKeyboardButton(text='11', callback_data="11_q_order"),
             InlineKeyboardButton(text='12', callback_data="12_q_order")) \
        .row(InlineKeyboardButton(text='13', callback_data="13_q_order"))

    return orderWorkUnsuccessKeyboard


# KEYBOARD FROM CHOOSE ORDER WORK IN CASPIAN TECH
async def order_work_command():
    orderKeyboard = InlineKeyboardMarkup()
    orderKeyboard.row(InlineKeyboardButton(text="Сайт", callback_data='site'))\
        .row(InlineKeyboardButton(text="Мобильное приложение", callback_data="mobile"))\
        .row(InlineKeyboardButton(text="Telegram Bot", callback_data="tg_bot"))

    return orderKeyboard
