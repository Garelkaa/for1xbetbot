import asyncio
import time
from middlewares.middlewares import CheckAdmin
from signature import bot, dp, db
from aiogram import Router, types
from aiogram.filters import Command
import datetime
from pytz import UTC
import logging
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin = Router(name='admin')
admin.message.middleware(CheckAdmin())


@admin.callback_query(lambda callback_query: callback_query.data.startswith('accept_add'))
async def accept_user(callback_query: types.CallbackQuery):
    data = callback_query.data
    telegram_id = data.split('_')[2]
    sum_str = data.split('_')[3]
    
    try:
        sum_val = float(sum_str)
    except ValueError:
        await bot.send_message(callback_query.message.chat.id, "Invalid sum value.")
        return
    
    text = callback_query.message.text
    bonus = db.get_bonus_user(callback_query.from_user.id)
    
    if bonus:
        bonus_multiplier = bonus / 100
    else:
        bonus_multiplier = 0.0  # No bonus applied if bonus is None

    # Calculate the total amount to be added to the balance
    total_amount = sum_val + (sum_val * bonus_multiplier)
    
    current_time = datetime.datetime.now(UTC)
    message_time = callback_query.message.date.replace(tzinfo=UTC)
    time_difference = current_time - message_time
    minutes = time_difference.total_seconds() // 60
    seconds = time_difference.total_seconds() % 60
    
    db.add_balance(telegram_id, total_amount)
    
    await bot.edit_message_text(f"{text}" + f"\n\n(ЗАЯВКА ОДОБРЕНА!)\nВремя принятия решения: {int(minutes)} минут {int(seconds)} секунд", callback_query.message.chat.id, callback_query.message.message_id, reply_markup=None)
    await bot.send_message(telegram_id, f"""Ваш счет успешно пополнен!
Удачной игры и больших выигрышей
Спасибо что выбираете нашу кассу""")
    db.add_balance_stats(telegram_id, sum=total_amount, date=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


@admin.callback_query(lambda callback_query: callback_query.data.startswith('decline_add'))
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


@admin.callback_query(lambda callback_query: callback_query.data.startswith('accept_widthraw'))
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

@admin.callback_query(lambda callback_query: callback_query.data.startswith('decline_widthraw'))
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
    
    
@admin.message(Command('али'))
async def req_ali(message: types.Message):
    db.change_req(new_req=4444111122225555)
    await message.answer("Реквезиты сменены для Али!")
    
@admin.message(Command('бека'))
async def req_ali(message: types.Message):
    db.change_req(new_req=4444222233334444)
    await message.answer("Реквезиты сменены для Бека!")
    
@admin.message(Command('майрамбек'))
async def req_ali(message: types.Message):
    db.change_req(new_req=9999111144448888)
    await message.answer("Реквезиты сменены для Майрамбек!")
    
@admin.message(Command('салам'))
async def req_ali(message: types.Message):
    db.change_req(new_req=2222666633331111)
    await message.answer("Реквезиты сменены для Салам!")
    

@admin.message(Command('подозрительный'))
async def suspicious_id(message: types.Message):
    args = message.text.split()
    db.add_suspicious(user_id=args[1])
    await message.answer("Пользователь занесен в список подозрительных")


@admin.message(Command('список_подозеваемых'))
async def list_of_suspicious(message: types.Message):
    suspicious_users = "".join(db.get_stats_suspicious())
    await message.answer(suspicious_users)


@admin.message(Command('бан'))
async def ban_user(message: types.Message):
    args = message.text.split()
    user_id = int(args[1])
    time_in_seconds = int(args[2])

    db.add_ban(user_id, time_in_seconds)
    await message.reply(f"Вы выдали бан на {time_in_seconds} секунд.")

    await asyncio.sleep(time_in_seconds)
    db.remove_ban(user_id)
    

@admin.message(Command('снять_бан'))
async def ban_user(message: types.Message):
    args = message.text.split()
    user_id = int(args[1])
    db.remove_ban(user_id)
    await message.reply(f"Бан снят.")
    

@admin.message(Command("отправить"))
async def send_message_private(message: types.Message):
    args = message.text.split()
    text = ' '.join(args[2:])
    await message.answer("Сообщение успешно отправлено")
    await bot.send_message(args[1], f"{text}")
    
    
start_time = time.time()

@admin.message(Command("клиентлист"))
async def client_list(message: types.Message):
    current_time = time.time()
    uptime_seconds = current_time - start_time

    # Convert uptime to hours, minutes, seconds
    uptime_hours = int(uptime_seconds // 3600)
    uptime_minutes = int((uptime_seconds % 3600) // 60)
    uptime_seconds = int(uptime_seconds % 60)

    # Create uptime message
    uptime_message = f"Бот работает уже {uptime_hours} часов, {uptime_minutes} минут и {uptime_seconds} секунд."

    # Send the uptime message
    await message.answer(uptime_message)
    

@admin.message(Command("Сколько"))
async def how_match(message: types.Message):
    args = message.text.split()
    
    if len(args) > 1 and args[1].lower() == 'сегодня':
        profit_today = db.get_today_profit()
        await message.reply(f"Прибыль за сегодня: {profit_today} рублей")
    else:
        total_profit = db.get_total_profit()
        await message.reply(f"Общая прибыль: {total_profit} рублей")
        
        
@admin.message(Command("Запустить_пополнение"))
async def start_replanish(message: types.Message):
    await message.reply("Пополнение запущено")
    db.change_replanis(1)


@admin.message(Command("Остановить_пополнение"))
async def stop_replanish(message: types.Message):
    await message.reply("Пополнение остановлено")
    db.change_replanis(0)
    

@admin.message(Command('рассылка'))
async def send_broadcast(message: types.Message):
    command_text = message.text
    args = command_text.split(maxsplit=1)[1] if len(command_text.split(maxsplit=1)) > 1 else ""

    if not args:
        await message.reply("Пожалуйста, укажите текст для рассылки.")
        return
    
    # Разбираем аргументы
    parts = args.split('(', 1)
    text = parts[0].strip()
    button_text = None
    button_url = None

    if len(parts) > 1:
        button_args = parts[1].rstrip(')')
        if ', ' in button_args:
            button_text, button_url = button_args.split(', ', 1)
        else:
            await message.reply("Пожалуйста, укажите параметры кнопки в формате: Текст, URL")
            return
    
    # Создаем инлайн клавиатуру, если есть параметры кнопки
    markup = None
    if button_text and button_url:
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=button_text, url=button_url)]
        ])

    # Получаем список пользователей из базы данных
    user_ids = db.get_all_users()

    for user_id in user_ids:
        try:
            await bot.send_message(user_id, text, reply_markup=markup)
        except Exception as e:
            logging.error(f"Не удалось отправить сообщение пользователю {user_id}: {e}")

    await message.reply("Рассылка завершена.")
    

@admin.message(Command("обновить"))
async def update_bonus(message: types.Message):
    db.update_ranking()