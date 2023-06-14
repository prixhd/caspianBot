from aiogram import Bot, Dispatcher, types, executor
import aiogram.utils.markdown as md

from keyboards import start_command, changes_command, order_work_command, form_for_team_unsuccess_command, order_work_unsuccess_command
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv, find_dotenv
import os
from validation import emailVal, numberVal
from sendMessage import send_email
from database import db

load_dotenv(find_dotenv())
bot = Bot(token=os.getenv('BOT_TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class FormForTeam(StatesGroup):
    name = State()
    number = State()
    about = State()


class OrderWork(StatesGroup):
    name = State()
    email = State()
    name_your_company = State()
    your_web_before = State()
    services_on_your_web = State()
    reg_company = State()
    aud_company = State()
    advantages_company = State()
    competitor_your_company = State()
    requirement_design = State()
    struct_web = State()
    should_be_on_web = State()
    web_you_like = State()


casData = db.Data('database/db.db')


@dp.message_handler(commands="start")
async def start(message: types.Message):
    keyboard = await start_command()
    if not casData.user_exists(message.from_user.id):
        casData.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, 'Добро пожаловать в нашего телеграмм бота компании Caspian Tech! '
                                                     'Мы очень рады приветствовать Вас здесь и надеемся, что наш бот будет полезным инструментом для Вашего бизнеса.\n\n'
                                                     'Мы специализируемся на создании профессиональных сайтов, которые помогут Вам привлечь новых клиентов и развивать свой бизнес в сети. '
                                                     'С помощью нашего бота Вы можете узнать о наших услугах, задать любые вопросы и получить индивидуальную консультацию. '
                                                     'Мы всегда готовы помочь Вам в создании уникального и качественного сайта, который будет соответствовать всем Вашим требованиям.\n\n'
                                                     'Выберите что вам нужно ↓', reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, 'Добро пожаловать в нашего телеграмм бота компании Caspian Tech! '
                                                     'Мы очень рады приветствовать Вас здесь и надеемся, что наш бот будет полезным инструментом для Вашего бизнеса.\n\n'
                                                     'Мы специализируемся на создании профессиональных сайтов, которые помогут Вам привлечь новых клиентов и развивать свой бизнес в сети. '
                                                     'С помощью нашего бота Вы можете узнать о наших услугах, задать любые вопросы и получить индивидуальную консультацию. '
                                                     'Мы всегда готовы помочь Вам в создании уникального и качественного сайта, который будет соответствовать всем Вашим требованиям.\n\n'
                                                     'Выберите что вам нужно ↓', reply_markup=keyboard)


@dp.message_handler(commands="call")
async def call_operator(message: types.Message):
    await bot.send_contact(message.from_user.id, '79777777777', 'Вишня')

# ---------------------------------------------------------------------------------------------------------------
# ЗАПОЛНЕНИЕ ФОРМЫ, ПО ЗАЯВКЕ В КОМАНДУ CASPIAN TECH
# ---------------------------------------------------------------------------------------------------------------


@dp.message_handler(Text(equals='Стать частью команды CaspianTech'))
async def form_for_team(message: types.Message):
    await FormForTeam.name.set()
    await bot.send_message(message.from_user.id, 'Хорошо, тогда давайте заполним небольшую форму🙂\n'
                                                 'Отвечайте на все вопросы одним сообщением!\n\n'
                                                 'Как вас зовут?')


# STATE ПОСТАВЛЕН НА ИМЯ
@dp.message_handler(state=FormForTeam.name)
async def form_for_team_process_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        if casData.get_signup(message.from_user.id) == "setnickname":
            casData.set_nickname(message.from_user.id, message.text)
            casData.set_signup(message.from_user.id, "done")

    await FormForTeam.next()
    await message.answer("Хорошо, теперь напишите нам ваш номер телефона:")


# STATE ПОСТАВЛЕН НА ПОЧТУ, ПРОВЕРКА НА ПРАВИЛЬНОСТЬ ВВОДА
# @dp.message_handler(lambda message: not emailVal(message.text), state=FormForTeam.email)
# async def form_for_team_process_email_invalid(message: types.Message):
#     await message.reply('Введите настоящую почту')
#
#
# @dp.message_handler(lambda message: emailVal(message.text), state=FormForTeam.email)
# async def form_for_team_process_email(message: types.Message, state: FSMContext):
#     await FormForTeam.next()
#     await state.update_data(
#         email=message.text
#     )
#
#     await message.answer('Теперь, введите свой номер телефона, для связи с вами:')


# STATE ПОСТАВЛЕН НА НОМЕР И ПРОВЕРКА НА ПРАВИЛЬНОСТЬ ВВОДА
@dp.message_handler(lambda message: not numberVal(message.text), state=FormForTeam.number)
async def form_form_team_process_number_invalid(message: types.Message):
    await message.reply('Введите настоящий номер телефона!')


@dp.message_handler(lambda message: numberVal(message.text), state=FormForTeam.number)
async def form_form_team_process_number(message: types.Message, state: FSMContext):
    await FormForTeam.next()
    await state.update_data(
        number=int(message.text)
    )

    await message.reply(
        'И наконец расскажи что-нибудь о себе, как о программисте!(Твои достижения,навыки, где ты учился и т.д.)')


# STATE ПОСТАВЛЕН НА БЛОКЕ "О СЕБЕ" А ТАКЖЕ ВЫВОДИТСЯ ВСЯ ФОРМА И ОТПРАКЛЯЕТСЯ СООБЩЕНИЕ НА ПОЧТУ
@dp.message_handler(state=FormForTeam.about)
async def form_form_team_process_about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
        keyboard = await changes_command()

        messages = "Заявка на поступление в команду: \n\n" \
                   f"1. Имя: {data['name']}\n" \
                   f"2. Номер телефона: {data['number']}\n" \
                   f"3. О себе: {data['about']}"

        await bot.send_message(message.from_user.id,
                               f'{messages}\n\n'
                               f'Проверьте, свое резюме.\n'
                               f'Все верно?',
                               reply_markup=keyboard)


@dp.callback_query_handler(lambda answer: answer.data == "yes_changes", state=FormForTeam)
async def form_for_team_success(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        messages = "Заявка на поступление в команду: \n\n" \
                   f"1. Имя: {data['name']}\n" \
                   f"2. Номер телефона: {data['number']}\n" \
                   f"3. О себе: {data['about']}\n"

        send_email(message=messages)

        await bot.send_message(message.from_user.id,
                               f'Отлично, спасибо что оставили свое резюме!\n'
                               'Мы рассмотрим его в ближайшее время и свяжемся с вами😉')

        await state.finish()


@dp.callback_query_handler(lambda answer: answer.data == "no_changes", state=FormForTeam)
async def form_for_team_unsuccess(message: types.Message):
    keyboard = await form_for_team_unsuccess_command()
    await bot.send_message(message.from_user.id,
                           "Хорошо, тогда выберите какой ответ на вопрос вы хотите изменить ↓",
                           reply_markup=keyboard)


@dp.callback_query_handler(lambda answer: answer.data == "first_question_form", state=FormForTeam)
async def form_for_team_change_first(message: types.Message):
    await FormForTeam.name.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить имя, введите имя и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "second_question_form", state=FormForTeam)
async def form_for_team_change_third(message: types.Message):
    await FormForTeam.number.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить номер телефона, введите номер и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "third_question_form", state=FormForTeam)
async def form_for_team_change_fourth(message: types.Message):
    await FormForTeam.about.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить блок 'о себе', распишите его заново: ")


# ----------------------------------------------------------------------------------------------------------------
# КОНЕЦ ЗАПОЛНЕНИЕ ФОРМЫ В CASPIANTECH
# ----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
# НАЧАЛО ЗАКАЗА РАБОТЫ В CASPIANTECH
# -----------------------------------------------------------------------------------------------------------------

@dp.message_handler(Text(equals="Заказать работу"))
async def order_work(message: types.Message):
    keyboard = await order_work_command()
    await bot.send_message(message.from_user.id, "Спасибо, что решили выбрать нашу компанию!\n"
                                                 "Вам нужно ответить на 14 вопрос\n"
                                                 "Выберите товар, который хотите заказать ↓", reply_markup=keyboard)


@dp.callback_query_handler(lambda a: a.data == "site")
async def order_work_site(message: types.Message):
    await OrderWork.name.set()
    await bot.send_message(message.from_user.id, "Так, хорошо давайте пройдем небольшой бриф, "
                                                 "благодаря которому мы поймем, какой сайт вам нужен. \n\n"
                                                 "Для начала введите свое имя:")


@dp.message_handler(state=OrderWork.name)
async def order_work_site_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        if casData.get_signup(message.from_user.id) == "setnickname":
            casData.set_nickname(message.from_user.id, message.text)
            casData.set_signup(message.from_user.id, "done")

    await OrderWork.next()
    await message.answer("Хорошо, теперь напишите нам вашу почту, для связи с вами:")


@dp.message_handler(lambda message: not emailVal(message.text), state=OrderWork.email)
async def order_work_site_process_email_invalid(message: types.Message):
    await message.reply('Введите настоящую почту')


@dp.message_handler(lambda message: emailVal(message.text), state=OrderWork.email)
async def order_work_site_process_email_success(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        email=message.text
    )

    await message.answer('Как называется ваша компания?')


@dp.message_handler(state=OrderWork.name_your_company)
async def order_work_site_name_company(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        name_your_company=message.text
    )

    await message.answer('Был ли у вас до этого сайт? (укажите ссылку)')


@dp.message_handler(state=OrderWork.your_web_before)
async def order_work_site_web_before(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        your_web_before=message.text
    )

    await message.answer('Какие виды услуг оказывает ваша компания?')


@dp.message_handler(state=OrderWork.services_on_your_web)
async def order_work_site_services_your_web(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        services_on_your_web=message.text
    )

    await message.answer('Какие регионы охватывает ваша компания?')


@dp.message_handler(state=OrderWork.reg_company)
async def order_work_site_reg_company(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        reg_company=message.text
    )

    await message.answer('Какая целевая аудитория у  вашей компании?')


@dp.message_handler(state=OrderWork.aud_company)
async def order_work_site_aud_company(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        aud_company=message.text
    )

    await message.answer('Какие у вас есть конкурентные преимущества ?')


@dp.message_handler(state=OrderWork.advantages_company)
async def order_work_site_advantages_company(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        advantages_company=message.text
    )

    await message.answer('Приведите сайт конкурентов')


@dp.message_handler(state=OrderWork.competitor_your_company)
async def order_work_site_competitor_company(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        competitor_your_company=message.text
    )

    await message.answer('Какие требования по дизайну сайта?')


@dp.message_handler(state=OrderWork.requirement_design)
async def order_work_site_requirement_design(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        requirement_design=message.text
    )

    await message.answer('Какие требования по структуре сайта?')


@dp.message_handler(state=OrderWork.struct_web)
async def order_work_site_struct_web(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        struct_web=message.text
    )

    await message.answer('Что обязательно должно быть  на вашем сайте?')


@dp.message_handler(state=OrderWork.should_be_on_web)
async def order_work_site_should_be_on_web(message: types.Message, state: FSMContext):
    await OrderWork.next()
    await state.update_data(
        should_be_on_web=message.text
    )

    await message.answer('Есть примеры сайтов которые нравятся вам по визуалу и по функционалу?')


@dp.message_handler(state=OrderWork.web_you_like)
async def order_work_site_web_you_like(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['web_you_like'] = message.text

        messages = "Заявка на заказ работы: \n\n" \
                   f"1. Имя: {data['name']}\n" \
                   f"2. Почта: {data['email']}\n" \
                   f"3. Название вашей компании: {data['name_your_company']}\n" \
                   f"4. Был ли у вас сайт раньше: {data['your_web_before']}\n" \
                   f"5. Услуги предоставляемые нашей компанией: {data['services_on_your_web']}\n" \
                   f"6. Какие регионы охватывает ваша компания: {data['reg_company']}\n" \
                   f"7. Какая целевая аудитория у  вашей компании: {data['aud_company']}\n" \
                   f"8. Какие у вас есть конкурентные преимущества: {data['advantages_company']}\n" \
                   f"9. Приведите сайт конкурентов: {data['competitor_your_company']}\n" \
                   f"10. Какие требования по дизайну сайта: {data['requirement_design']}\n" \
                   f"11. Какие требования по структуре сайта: {data['struct_web']}\n" \
                   f"12. Что обязательно должно быть  на вашем сайте: {data['should_be_on_web']}\n" \
                   f"13. Примеры сайтов которые нравятся вам по визуалу и по функционалу: {data['web_you_like']}\n" \

        send_email(message=messages)

        keyboard = await changes_command()

        await bot.send_message(message.from_user.id, f'{messages}\n\n'
                                                     f'Спасибо, что прошли этот бриф!\n'
                                                     'Проверьте правильность введенных вами данных!\n\n'
                                                     f'Все верно?', reply_markup=keyboard)


@dp.callback_query_handler(lambda answer: answer.data == "yes_changes", state=OrderWork)
async def order_work_site_yes_change(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        messages = "Заявка на заказ работы: \n\n" \
                   f"1. Имя: {data['name']}\n" \
                   f"2. Почта: {data['email']}\n" \
                   f"3. Название вашей компании: {data['name_your_company']}\n" \
                   f"4. Был ли у вас сайт раньше: {data['your_web_before']}\n" \
                   f"5. Услуги предоставляемые нашей компанией: {data['services_on_your_web']}\n" \
                   f"6. Какие регионы охватывает ваша компания: {data['reg_company']}\n" \
                   f"7. Какая целевая аудитория у  вашей компании: {data['aud_company']}\n" \
                   f"8. Какие у вас есть конкурентные преимущества: {data['advantages_company']}\n" \
                   f"9. Приведите сайт конкурентов: {data['competitor_your_company']}\n" \
                   f"10. Какие требования по дизайну сайта: {data['requirement_design']}\n" \
                   f"11. Какие требования по структуре сайта: {data['struct_web']}\n" \
                   f"12. Что обязательно должно быть  на вашем сайте: {data['should_be_on_web']}\n" \
                   f"13. Примеры сайтов которые нравятся вам по визуалу и по функционалу: {data['web_you_like']}\n"

        send_email(message=messages)

        await bot.send_message(message.from_user.id,
                               f'Отлично, спасибо что оставили свое резюме!\n'
                               'Мы рассмотрим его в ближайшее время и свяжемся с вами😉')

        await state.finish()


@dp.callback_query_handler(lambda answer: answer.data == "no_changes", state=OrderWork)
async def order_work_site_no_change(message: types.Message):
    keyboard = await order_work_unsuccess_command()

    await bot.send_message(message.from_user.id,
                           "Хорошо, тогда выберите какой ответ на вопрос вы хотите изменить ↓",
                           reply_markup=keyboard)


@dp.callback_query_handler(lambda answer: answer.data == "1_q_order", state=OrderWork)
async def order_work_change_1(message: types.Message):
    await OrderWork.name.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить первый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "2_q_order", state=OrderWork)
async def order_work_change_2(message: types.Message):
    await OrderWork.email.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить второй вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "3_q_order", state=OrderWork)
async def order_work_change_3(message: types.Message):
    await OrderWork.name_your_company.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить третий вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "4_q_order", state=OrderWork)
async def order_work_change_4(message: types.Message):
    await OrderWork.your_web_before.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить 4 вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "5_q_order", state=OrderWork)
async def order_work_change_5(message: types.Message):
    await OrderWork.services_on_your_web.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить пятый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "6_q_order", state=OrderWork)
async def order_work_change_6(message: types.Message):
    await OrderWork.reg_company.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить шестой вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "7_q_order", state=OrderWork)
async def order_work_change_7(message: types.Message):
    await OrderWork.aud_company.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить седьмой вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "8_q_order", state=OrderWork)
async def order_work_change_8(message: types.Message):
    await OrderWork.advantages_company.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить восьмой вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "9_q_order", state=OrderWork)
async def order_work_change_9(message: types.Message):
    await OrderWork.competitor_your_company.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить девятый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "10_q_order", state=OrderWork)
async def order_work_change_10(message: types.Message):
    await OrderWork.requirement_design.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить десятый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "11_q_order", state=OrderWork)
async def order_work_change_11(message: types.Message):
    await OrderWork.struct_web.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить одиннадцатый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "12_q_order", state=OrderWork)
async def order_work_change_12(message: types.Message):
    await OrderWork.should_be_on_web.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить двенадцатый вопрос, введите его и следующие вопросы снова: ")


@dp.callback_query_handler(lambda answer: answer.data == "13_q_order", state=OrderWork)
async def order_work_change_13(message: types.Message):
    await OrderWork.web_you_like.set()
    await bot.send_message(message.from_user.id, "Вы хотите изменить тринадцатый вопрос, введите его и следующие вопросы снова: ")
# ----------------------------------------------------------------------------------------------------------------
# КОНЕЦ ЗАКАЗЫ РАБОТЫ В CASPIANTECH
# ----------------------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
