from signature import bot, FSMContext, State, StatesGroup, dp
from handlers.client import user
from aiogram import F, types
from keyboard.client_kb import choose_bank, paid_keyboard, choice_bank_withdraw_nav
from keyboard.admin_kb import verif_add_balance, verif_widthraw_balance


class AddBalanceState(StatesGroup):
    sum = State()
    id_xbet = State()
    photo = State()
    
    
class WithdrawBalanceState(StatesGroup):
    id_xbet = State()
    bank_choice = State()
    code = State()
    number_card = State()
    

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
    username = callback_query.from_user.first_name
    sum_value = user_data.get('sum')
    id_xbet = user_data.get('id_xbet')

    admin_message = (f"Чат ID: {callback_query.from_user.id}\n"
                     f"Чел: @{username}\n"
                     f"1XBET ID: {id_xbet}\n"
                     f"Сумма пополнения: {sum_value}\n"
                     f"Способ пополнения: MBANK\n"
                     f"Без бонуса: {sum_value}")
    photo = callback_query.photo[-1]
    
    await bot.send_photo(-4200018730, photo=photo.file_id)
    await bot.send_message(-4200018730, f"{admin_message}", reply_markup=verif_add_balance(callback_query.from_user.id, sum_value))
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
    
@user.message(F.text == 'Вывести средства')
async def withdraw_balance(message: types.Message, state: FSMContext):
    await message.answer("""
Укажите удобный вам способ снятия средств со счета

Выберите банк:""", reply_markup=choice_bank_withdraw_nav())
    await state.set_state(WithdrawBalanceState.bank_choice)

@dp.callback_query(F.data.startswith('choose_bank_'), WithdrawBalanceState.bank_choice)
async def choice_bank_withdraw(call: types.CallbackQuery, state: FSMContext):
    selected_bank = call.data.split('choose_bank_')[1].replace("_", " ").upper()
    await state.update_data(selected_bank=selected_bank)
    await bot.send_message(call.from_user.id, f"Введите реквизиты для выбранного вами банка ({selected_bank}):")
    await state.set_state(WithdrawBalanceState.number_card)

@dp.message(WithdrawBalanceState.number_card)
async def number_card(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo="AgACAgIAAxkBAANiZmF9YuMR_xQbwsWT3cRdONGzlWAAAl_bMRuRQQhL6Dafmzq-jV0BAAMCAAN5AAM1BA", caption="Введите ваш ID (номер счета от 1XBET)")
    await state.update_data(number_card=message.text)
    await state.set_state(WithdrawBalanceState.id_xbet)

@dp.message(WithdrawBalanceState.id_xbet)
async def withdraw_id_xbet(message: types.Message, state: FSMContext):
    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAPKZmHezWlME5qm8PSW-kZO6Gnms0wAAv3gMRsvIxFLd70cfQVWcHgBAAMCAAN4AAM1BA')
    await bot.send_photo(message.from_user.id, photo='AgACAgIAAxkBAAPMZmHe9-abu4UsE_HlXdDPZEC9YJoAAv7gMRsvIxFLJ6gbeo5dBk4BAAMCAAN4AAM1BA', caption="Выберете в 1XBET способ вывода наличными, потом выберите терминал: XBoss (24/7)")
    await bot.send_message(message.from_user.id, "Введите код")
    await state.update_data(id_xbet=message.text)
    await state.set_state(WithdrawBalanceState.code)

@dp.message(WithdrawBalanceState.code)
async def input_code(message: types.Message, state: FSMContext):
    code = message.text
    if not (len(code) == 4 and code.isalnum() and code.isascii()):
        await bot.send_message(message.from_user.id, "Код от 1XBET обычно содержит 4 символа с латинскими буквами/цифрами, введите корректный код!")
    else:
        await state.update_data(code=code)
        user_data = await state.get_data()
        id_xbet = user_data.get('id_xbet')
        number_card = user_data.get('number_card')
        selected_bank = user_data.get('selected_bank')
        await bot.send_message(message.from_user.id, f"""✅Ваша заявка принята на проверку!

Ваш кошелек: {id_xbet}
🆔Номер ID (1XBET): {id_xbet}

💰Комиссия: 0% 
Способ: {selected_bank}
Код: {code}

⚠️ Вывод занимает от 1 секунды до 10 минут.

Пожалуйста, подождите!

✅Вы получите уведомление о зачислении средств от админ бота!""")
        await state.clear()
        await bot.send_message(-4200018730, f"""Чат ID: {message.from_user.id}
Чел: {message.from_user.first_name}
1XBET ID: {id_xbet}
Секретный код: {code}
Способ снятия: {selected_bank}
Рекизиты: {number_card}""" , reply_markup=verif_widthraw_balance(message.from_user.id))