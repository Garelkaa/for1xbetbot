from signature import bot, dp
from aiogram import types
from keyboard.chat_kb import chat_by_kb
from datetime import datetime


@dp.callback_query()
async def check_sub(message: types.CallbackQuery):
    chat_member = await bot.get_chat_member(chat_id=-1002242167058, user_id=message.from_user.id)
    if chat_member.status == 'left':
        await bot.send_message(message.from_user.id,
            f"Для продолжения пользования этим ботом - подпишитесь на наш канал!", reply_markup=chat_by_kb()
        )
    else:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        await bot.send_message(message.from_user.id, f"""
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