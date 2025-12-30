from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎯 Test baslaw")],
            [KeyboardButton(text="📊 Meniń nátiyjelerim")]
        ],
        resize_keyboard=True
    )

def test_options():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="A", callback_data="ans_a"),
                InlineKeyboardButton(text="B", callback_data="ans_b")
            ],
            [
                InlineKeyboardButton(text="C", callback_data="ans_c"),
                InlineKeyboardButton(text="D", callback_data="ans_d")
            ],
            [
                InlineKeyboardButton(text="⬅️ Artqa", callback_data="ans_back"),
                InlineKeyboardButton(text="➡️ Keyingi soraw", callback_data="ans_next")
            ]
        ]
    )
