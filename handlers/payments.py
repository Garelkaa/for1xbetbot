from signature import bot, FSMContext, State, StatesGroup, dp
from handlers.client import user
from aiogram import F, types
from keyboard.client_kb import choose_bank, paid_keyboard
from aiogram.types.input_file import InputFile


class AddBalanceState(StatesGroup):
    sum = State()
    id_xbet = State()
    photo = State()
    

@user.message(F.text == 'Пополнить баланс')
async def add_balance(message: types.Message):
    await message.answer("Укажите удобный вам способ пополнения счета\n\nВыберите банк:", reply_markup=choose_bank())

@user.callback_query(lambda c: c.data == 'choose_bank_mbank')
async def new_sum(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer("Введите сумму для пополнения счета")
    await state.set_state(AddBalanceState.sum)

@dp.message(AddBalanceState.sum)
async def input_id(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo="AgACAgIAAxkBAANiZmF9YuMR_xQbwsWT3cRdONGzlWAAAl_bMRuRQQhL6Dafmzq-jV0BAAMCAAN5AAM1BA", caption="Введите ваш ID(номер счета от 1XBET)")
    await state.update_data(sum=message.text)
    await state.set_state(AddBalanceState.id_xbet)

@dp.message(AddBalanceState.id_xbet)
async def wait_pay(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    sum_value = user_data.get('sum')
    await message.answer(f"""Отправьте {sum_value} сомов по следующим реквизитам "MBANK":
После перевода нажмите "Я оплатил"

+996 502073454""", reply_markup=paid_keyboard())
    await state.update_data(id_xbet=message.text)
    
    

@dp.callback_query(lambda c: c.data == 'i_have_paid')
async def send_photo_pay(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.send_message(callback_query.from_user.id, f"""Отправьте скриншот чека операции!
❗️Фотография должна быть четкой, на ней должны быть видны дата и время проведения операции, иначе вашу заявку не получится обработать!❗️""")
    await state.set_state(AddBalanceState.photo)
    
@dp.message(F.photo, AddBalanceState.photo)
async def confirm_payment(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    username = callback_query.from_user.username
    sum_value = user_data.get('sum')
    id_xbet = user_data.get('id_xbet')

    admin_message = (f"Чат ID: {callback_query.from_user.id}\n"
                     f"Чел: @{username}\n"
                     f"1XBET ID: {id_xbet}\n"
                     f"Сумма пополнения: {sum_value}\n"
                     f"Способ пополнения: MBANK\n"
                     f"Без бонуса: {sum_value}")
    photo = callback_query.photo[-1]
    
    await bot.send_photo(-4200018730, photo=photo.file_id, caption=admin_message)
    await state.clear()
    await callback_query.answer(f"""✅Ваша заявка принята на проверку!

Ваш кошелек: {id_xbet}
🆔Номер ID (1XBET): {id_xbet}
💵Сумма: {sum_value}
💵Сумма с учетом бонуса: {sum_value}
Способ: MBANK

⚠️ Пополнение занимает от 1 секунды до 15 минут.
(Если ваша заявка не будет обработана в течение 15 минут, то мы сделаем БОНУС к вашему депозиту +30%)‼
Пожалуйста подождите!

✅Вы получите уведомление о зачислении средств!""")