from signature import bot, dp, db
from aiogram import types
import datetime
from pytz import UTC


@dp.callback_query(lambda callback_query: callback_query.data.startswith('accept_add'))
async def accept_user(callback_query: types.CallbackQuery):
    data = callback_query.data
    telegram_id = data.split('_')[2]
    sum = data.split('_')[3]
    text = callback_query.message.text
    
    current_time = datetime.datetime.now(UTC)
    
    message_time = callback_query.message.date.replace(tzinfo=UTC)

    time_difference = current_time - message_time
    
    minutes = time_difference.total_seconds() // 60
    seconds = time_difference.total_seconds() % 60
    
    await bot.edit_message_text(f"{text}" + f"\n\n(ЗАЯВКА ОДОБРЕНА!)\nВремя принятия решения: {int(minutes)} минут {int(seconds)} секунд", callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
    await bot.send_message(telegram_id, f"""Ваш счет успешно пополнен!
Удачной игры и больших выигрышей
Спасибо что выбираете нашу кассу""")
    db.add_balance_stats(telegram_id, sum=sum, date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

@dp.callback_query(lambda callback_query: callback_query.data.startswith('decline_add'))
async def decline_user(callback_query: types.CallbackQuery):
    data = callback_query.data
    telegram_id = data.split('_')[2]
    text = callback_query.message.text
    
    current_time = datetime.datetime.now(UTC)
    
    message_time = callback_query.message.date.replace(tzinfo=UTC)

    time_difference = current_time - message_time
    
    minutes = time_difference.total_seconds() // 60
    seconds = time_difference.total_seconds() % 60
    
    await bot.edit_message_text(f"{text}" + f"\n\n(ЗАЯВКА ОТКЛОНЕНА!)\nВремя принятия решения: {int(minutes)} минут {int(seconds)} секунд", callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
    await bot.send_message(telegram_id, f"""Ваш перевод до сих пор не поступил! X
Пожалуйста проверьте правильно ли вы ввели
реквизиты.
Если у вас возникли проблемы, свяжитесь с админом""")
    db.add_widthraw_stats(telegram_id, date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@dp.callback_query(lambda callback_query: callback_query.data.startswith('accept_widthraw'))
async def accept_user(callback_query: types.CallbackQuery):
    data = callback_query.data
    telegram_id = data.split('_')[2]
    text = callback_query.message.text
    
    current_time = datetime.datetime.now(UTC)
    
    message_time = callback_query.message.date.replace(tzinfo=UTC)

    time_difference = current_time - message_time
    
    minutes = time_difference.total_seconds() // 60
    seconds = time_difference.total_seconds() % 60
    
    await bot.edit_message_text(f"{text}" + f"\n\n(ЗАЯВКА ОДОБРЕНА!)\nВремя принятия решения: {int(minutes)} минут {int(seconds)} секунд", callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
    await bot.send_message(telegram_id, f"""Ваш счет успешно пополнен!
Удачной игры и больших выигрышей
Спасибо что выбираете нашу кассу""")

@dp.callback_query(lambda callback_query: callback_query.data.startswith('decline_widthraw'))
async def decline_user(callback_query: types.CallbackQuery):
    data = callback_query.data
    telegram_id = data.split('_')[2]
    text = callback_query.message.text
    
    current_time = datetime.datetime.now(UTC)
    
    message_time = callback_query.message.date.replace(tzinfo=UTC)

    time_difference = current_time - message_time
    
    minutes = time_difference.total_seconds() // 60
    seconds = time_difference.total_seconds() % 60
    
    await bot.edit_message_text(f"{text}" + f"\n\n(ЗАЯВКА ОТКЛОНЕНА!)\nВремя принятия решения: {int(minutes)} минут {int(seconds)} секунд", callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
    await bot.send_message(telegram_id, f"""Ваш перевод до сих пор не поступил! X
Пожалуйста проверьте правильно ли вы ввели
реквизиты.
Если у вас возникли проблемы, свяжитесь с админом""")
