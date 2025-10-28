from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="🌞 فال روزانه", callback_data="daily")
    kb.button(text="🌙 فال هفتگی", callback_data="weekly")
    kb.button(text="🌟 فال ماهانه", callback_data="monthly")
    kb.button(text="❤️ فال عشق", callback_data="love")
    kb.button(text="☕ فال قهوه", callback_data="coffee")
    kb.button(text="🃏 فال تاروت", callback_data="tarot")
    kb.adjust(2)
    return kb.as_markup()

def zodiac_menu():
    signs = [
        "♈ فروردین", "♉ اردیبهشت", "♊ خرداد", "♋ تیر",
        "♌ مرداد", "♍ شهریور", "♎ مهر", "♏ آبان",
        "♐ آذر", "♑ دی", "♒ بهمن", "♓ اسفند"
    ]
    kb = InlineKeyboardBuilder()
    for sign in signs:
        kb.button(text=sign, callback_data=f"sign_{sign}")
    kb.adjust(3)
    return kb.as_markup()

def donate_menu():
    kb = InlineKeyboardBuilder()
    kb.button(text="💎 حمایت با کریپتو", url="https://your-crypto-link.com")
    return kb.as_markup()
