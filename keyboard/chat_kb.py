from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def chat_by_kb():
    channel = InlineKeyboardButton(text='Наш канал', url='https://t.me/+eWaAKIPUIB0zMjI6')
    check_success = InlineKeyboardButton(text='Я подписался', callback_data='check_success')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [channel], [check_success],
    ])
    return markup