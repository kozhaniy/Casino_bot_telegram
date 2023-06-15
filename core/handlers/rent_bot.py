from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from core.keyboards.inline import you_ready
from core.Utils.states import Steps
from core.other.db_connect import Request
from aiogram.types import LabeledPrice, PreCheckoutQuery
from datetime import datetime, timedelta


async def buy_complete_rent_bot(message:Message, state: FSMContext, request: Request):
    data = await state.get_data()
    token: str = data['bot_token']
    bot_id: int = int(token.split(':')[0])
    you_kassa: str = data['youkassa_token']
    percent: str = data['percent']
    payment_data: str = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")


async def pre_check_rent_bot(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def get_youkassa_token(message: Message, bot: Bot, state: FSMContext, request: Request):
    await state.update_data(youkassa_token=message.text)
    youkassa_token = await request.get_youkassa_token(bot.id)
    price = [LabeledPrice(label='Аренда бота казино', amout=50000)]
    title = 'оплата за аренду бота yourcasino'
    description = 'Арендуй бота и начни зарабатывать прямо сейчас'
    await bot.send_invoice(chat_id=message.chat.id,
                           title=title,
                           description=description,
                           payload='yourccasino',
                           provider_token=youkassa_token,
                           currency='rub',
                           prices=price)
    await state.set_state(Steps.GET_PAYMENTS)



async def get_percent(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(f'{message.text} - это не число')
        return

    await state.update_data(percent=message.text)
    await message.answer('Теперь отправь ЮКасса токен')
    await state.set_state(Steps.GET_YOUKASSA_TOKEN)


async def get_token(message: Message, state: FSMContext):
    await state.update_data(bot_token=message.text)
    await message.answer('Теперь отправь процент рефералам')
    await state.set_state(Steps.GET_PERCENT)


async def start_rent_token(call: CallbackQuery, bot: Bot, state: FSMContext):
    await bot.answer_callback_query(call.id)
    await call.message.edit_text('Начинаем процедуру аренды бота', reply_markup=None)
    await call.message.answer(f'Отправь токен своего бота')
    await state.set_state(Steps.GET_TOKEN)


async def start_rent(message: Message):
    await message.answer(f"Начинаем оформлять аренду бота.\r\n"
                         f"Подготовь слудующие данные: \r\n"
                         f"1) Токен бота. Зарегистрируй своего бота через @botfather\r\n"
                         f"2) Процент отчисления рефералам\r\n"
                         f"3) Юкасса токен. Добавь платежный шлюз для своего бота в том же @botfather\r\n"
                         f"4) Оплата. Я вышлю тебе счет для оплаты аренды бота на меся\r\n\r\n"
                         
                         f"Как будешь готов жми на кнопку", reply_markup=you_ready)
