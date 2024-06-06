from signature import bot, dp
from aiogram import types, F
from keyboard.chat_kb import chat_by_kb
from datetime import datetime
from handlers.client import user


# @user.message(F.photo)
# async def photo(message: types.Message):
#     photo_data = message.photo[-1]
#     await message.answer(f"{photo_data}")


@dp.callback_query(lambda c: c.data == 'check_success')
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