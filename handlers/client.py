from signature import bot, dp 
from aiogram import Router, types
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
    

