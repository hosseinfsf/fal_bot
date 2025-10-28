import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters.text import Text
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# فال‌ها به صورت نمونه
horoscopes = {
    "1": "فال فروردین 🌸\nامروز روز پر انرژی‌ای داری.\nموفقیت‌های کوچک شمارو خوشحال می‌کنه.\nبه دوستانت توجه کن.\nیک تصمیم جدید بگیر.\nسعی کن مثبت باشی.\n#فروردین #فال",
    "2": "فال اردیبهشت 🌿\nامروز احساس آرامش داری.\nیک فرصت شغلی خوب میاد.\nمهارت‌هایت رو تقویت کن.\nبا صبر پیش برو.\nمراقب سلامتی باش.\n#اردیبهشت #فال",
    # ادامه تا 12
}

# کلیدهای ماه‌ها
def month_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [InlineKeyboardButton(f"{i}", callback_data=f"month_{i}") for i in range(1, 13)]
    keyboard.add(*buttons)
    return keyboard

@dp.message(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "سلام! 🌟\nفال امروزت رو انتخاب کن:",
        reply_markup=month_keyboard()
    )

@dp.callback_query(Text(startswith="month_"))
async def send_horoscope(query: types.CallbackQuery):
    month = query.data.split("_")[1]
    text = horoscopes.get(month, "فال موجود نیست 😢")
    await query.message.edit_text(text, reply_markup=month_keyboard())

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
