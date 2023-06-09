from aiogram import Bot, Dispatcher, types, executor
import aiogram.utils.markdown as md

from keyboards import start_command, form_for_team_command
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from validation import emailVal
from sendMessage import send_email

bot = Bot(token='6085427546:AAEfBDoQdY0D4LFTFBWPj7uKTKIx8gpFq4c')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FormForTeam(StatesGroup):
    name = State()
    email = State()
    number = State()
    about = State()


@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = await start_command()
    await message.answer('Добро пожаловать в нашего телеграмм бота компании Caspian Tech! '
                         'Мы очень рады приветствовать Вас здесь и надеемся, что наш бот будет полезным инструментом для Вашего бизнеса.\n\n'
                         'Мы специализируемся на создании профессиональных сайтов, которые помогут Вам привлечь новых клиентов и развивать свой бизнес в сети. '
                         'С помощью нашего бота Вы можете узнать о наших услугах, задать любые вопросы и получить индивидуальную консультацию. '
                         'Мы всегда готовы помочь Вам в создании уникального и качественного сайта, который будет соответствовать всем Вашим требованиям.\n\n'
                         'Выберите что вым нужно ↓', reply_markup=keyboard)


# ---------------------------------------------------------------------------------------------------------------
# ЗАПОЛНЕНИЕ ФОРМЫ, ПО ЗАЯВКЕ В КОМАНДУ CASPIAN TECH
# ---------------------------------------------------------------------------------------------------------------
@dp.message_handler(Text(equals='Стать частью команды CaspianTech'))
async def form_for_team(message: types.Message):
    await FormForTeam.name.set()
    await message.answer('Хорошо, тогда давайте заполним небольшую форму🙂\n\n'
                         'Как вас зовут?')


# STATE ПОСТАВЛЕН НА ИМЯ
@dp.message_handler(state=FormForTeam.name)
async def form_for_team_process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FormForTeam.next()
    await message.answer("Хорошо, теперь напишите нам вашу почту:")


# STATE ПОСТАВЛЕН НА ПОЧТУ, ПРОВЕРКА НА ПРАВИЛЬНОСТЬ ВВОДА
@dp.message_handler(lambda message: not emailVal(message.text), state=FormForTeam.email)
async def form_for_team_process_email_invalid(message: types.Message):
    await message.reply('Введите настоящую почту')


@dp.message_handler(lambda message: emailVal(message.text), state=FormForTeam.email)
async def form_for_team_process_email(message: types.Message, state: FSMContext):
    await FormForTeam.next()
    await state.update_data(
        email=message.text
    )

    await message.answer('Теперь, введите свой номер телефона, для связи с вами:')


# STATE ПОСТАВЛЕН НА НОМЕР И ПРОВЕРКА НА ПРАВИЛЬНОСТЬ ВВОДА
@dp.message_handler(lambda message: not message.text.isdigit(), state=FormForTeam.number)
async def form_form_team_process_number_invalid(message: types.Message):
    await message.reply('Введите верный номер телефона!')


@dp.message_handler(lambda message: message.text.isdigit(), state=FormForTeam.number)
async def form_form_team_process_number(message: types.Message, state: FSMContext):
    await FormForTeam.next()
    await state.update_data(number=int(message.text))

    await message.reply(
        'И наконец расскажи что-нибудь о себе, как о программисте!(Твои достижения,навыки, где ты учился и т.д.)')


# STATE ПОСТАВЛЕН НА БЛОКЕ "О СЕБЕ" А ТАКЖЕ ВЫВОДИТСЯ ВСЯ ФОРМА И ОТПРАКЛЯЕТСЯ СООБЩЕНИЕ НА ПОЧТУ
@dp.message_handler(state=FormForTeam.about)
async def form_form_team_process_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text

        messages = "Заявка на поступление в команду: \n\n" \
                   f"Имя: {data['name']}\n" \
                   f"Почта: {data['email']}\n" \
                   f"Номер телефона: {data['number']}\n" \
                   f"О себе: {data['about']}\n"

        # await bot.send_message(
        #     message.chat.id,
        #     md.text(
        #         md.text('Все верно?\n\nВаше имя: ', md.bold(data['name'])),
        #         md.text('E-mail: ', md.bold(data['email'])),
        #         md.text('Номер: ', md.bold(data['number']), '\n'),
        #         md.text('О вас: ', md.bold(data['about'])),
        #         sep='\n',
        #     ),
        #     parse_mode=ParseMode.MARKDOWN,
        # )

        send_email(message=messages)
        await message.answer('Отлично, спасибо что оставили свое резюме!\n'
                             'Мы рассмотрим его в ближайшее время и свяжемся с вами😉')

        await state.finish()


# ----------------------------------------------------------------------------------------------------------------
# КОНЕЦ ЗАПОЛНЕНИЕ ФОРМЫ В CASPIANTECH
# ----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
