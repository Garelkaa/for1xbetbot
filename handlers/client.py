from signature import bot, db
from aiogram import Router, types, F
from aiogram.filters.command import CommandStart
from middlewares.middlewares import CheckDb
from datetime import datetime
from aiogram.types import FSInputFile
from keyboard.client_kb import main_menu, stats_kb

user = Router(name='user')
user.message.middleware(CheckDb())

@user.message(CommandStart())
async def start_handler(message: types.Message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    await message.answer(f"""
                         Привет, {message.from_user.first_name}!
XBoss🇰🇬 поможет тебе пополнить или вывести средства в 1XBET

👨‍💻 Мы работаем 24/7
💸 0% комиссии!
🔒 Ваши операции под надежной защитой Финансовой службы!

💬 Наша служба поддержки:
@XBoss_KG

📢 Наш чат для общения:
https://t.me/kgXBoss_chat

📆 На {current_time}
Бот работает стабильно и заслуживает доверие пользователей! 🏆""", reply_markup=main_menu)
    

@user.message(F.text == '🎁 Бонусы')
async def bonus(message: types.Message):
    await bot.send_video(message.from_user.id, video=FSInputFile(r'/Users/andrijserbak/Desktop/workFolder/for1xbetbot/images/video.mp4'), caption=f"""Зарегистрировайтесь через наш
Промокод - XBoss5
И Получаете до 35000 Сомов (120%) На первый депозит!
Чтобы получить бонус вам нужно
1. Зарегистрироваться через наш
Промокод - XBoss5
2. Заполнить всё поля регистрационной анкеты + номер телефона.
3. Пополнить счёт через XBoss
@KgXBossBot
Шу Бонус до 120% - пополняйте счёт на сумму
129167 * 120% = 35000
25000 * 120% = 30000""")
    
    
@user.message(F.text == "📋 Статистика")
async def stats(message: types.Message):
    await bot.send_message(message.from_user.id, f"Какую статистику вы хотите посмотреть?", reply_markup=stats_kb)
    

@user.message(F.text == '💵 Пополнений')
async def add_balance_all_time(message: types.Message):
    await bot.send_message(message.from_user.id, f"".join(db.get_stats_add_balance(message.from_user.id)))
    
    
@user.message(F.text == '💸 Выводов')
async def add_balance_all_time(message: types.Message):
    await bot.send_message(message.from_user.id, f"".join(db.get_stats_widthraw_balance(message.from_user.id)))


@user.message(F.text == '🏆 Мой статус')
async def rate_user(message: types.Message):
    if db.get_rank_user(message.from_user.id):
        bonus = db.get_bonus_user(message.from_user.id)
        ranking = db.get_rank_user(message.from_user.id)
        response = (f"|. Ваш текущий статус: Базовый\n"
                    f"Ваше место в рейтинге: {ranking}\n"
                    f"§ Ваш персональный бонус: {bonus}%\n"
                    f"Рейтинг обновляется ежемесячно в начале и посередине месяца.\n"
                    f"Самые активные клиенты, отличающиеся суммарными депозитами, получают следующие бонусы:\n"
                    f"Топ-3 - 3%\n"
                    f"Топ-20 - 2%\n"
                    f"Топ-50 - 1%")
    
    await message.answer(response)
    