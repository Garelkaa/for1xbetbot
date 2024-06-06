from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def choose_bank():
    mbank = InlineKeyboardButton(text='MBANK', callback_data='choose_bank_mbank')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [mbank]
    ])
    
    return markup


def paid_keyboard():
    i_have_paid = InlineKeyboardButton(text='Я оплатил', callback_data='i_have_paid')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [i_have_paid]
    ])
    
    return markup