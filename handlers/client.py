from signature import bot, dp 
from aiogram import Router, types, F
from aiogram.filters.command import CommandStart
from middlewares.middlewares import CheckDb
from datetime import datetime

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
Бот работает стабильно и заслуживает доверие пользователей! 🏆""")
    

@user.message(F.text == 'Бонусы')
async def bonus(message: types.Message):
    await bot.send_video(message.from_user.id, video='', caption=f"""Зарегистрировайтесь через наш
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
