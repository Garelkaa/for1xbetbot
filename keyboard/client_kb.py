from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def choose_bank():
    mbank = InlineKeyboardButton(text='MBANK', callback_data='choose_bank_mbank')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [mbank]
    ])
    
    return markup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Пополнить баланс"),KeyboardButton(text="💸 Вывести средства")],
        [KeyboardButton(text="📋 Статистика"),KeyboardButton(text="🏆 Мой статус")],
        [KeyboardButton(text="🎁 Бонусы")],
    ],
    resize_keyboard=True
)

stats_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='💸 Выводов'), KeyboardButton(text='💵 Пополнений')]
    ],
    resize_keyboard=True
)

def choice_bank_withdraw_nav():
    banks = ['MBANK', 'QIWI', 'MegaPay', 'Optima bank', 'Balance kg', 'О!Деньги', 'Сбербанк', 'Элкарт', 'Элсом', "Единицы на сотовый"]
    buttons = [InlineKeyboardButton(text=bank, callback_data=f'choose_bank_{bank.lower().replace(" ", "_")}') for bank in banks]
    builder = InlineKeyboardBuilder()
    builder.row(*buttons, width=3)
    return builder.as_markup()

def paid_keyboard():
    i_have_paid = InlineKeyboardButton(text='✅ Я оплатил', callback_data='i_have_paid')
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [i_have_paid]
    ])
    
    return markup