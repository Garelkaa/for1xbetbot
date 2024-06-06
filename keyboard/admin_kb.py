from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton


def verif_add_balance(telegram_id, sum):
    accept = InlineKeyboardButton(
        text='✅ Принять', callback_data=f'accept_add_{telegram_id}_{sum}')
    decline = InlineKeyboardButton(
        text='❌ Отклонить', callback_data=f'decline_add_{telegram_id}')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [accept],
        [decline]
    ])
    return keyboard


def verif_widthraw_balance(telegram_id):
    accept = InlineKeyboardButton(
        text='✅ Принять', callback_data=f'accept_widthraw_{telegram_id}')
    decline = InlineKeyboardButton(
        text='❌ Отклонить', callback_data=f'decline_widthraw_{telegram_id}')

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [accept],
        [decline]
    ])
    return keyboard