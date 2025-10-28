import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters import Command, F
from dotenv import load_dotenv
import openai

# بارگذاری متغیرهای محیطی
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
openai.api_key = OPENAI_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ماه‌ها فارسی
months = {
    1: "فروردین", 2: "اردیبهشت", 3: "خرداد",
    4: "تیر", 5: "مرداد", 6: "شهریور",
    7: "مهر", 8: "آبان", 9: "آذر",
    10: "دی", 11: "بهمن", 12: "اسفند"
}

# دسته‌ها
categories = ["روزانه", "هفتگی", "ماهانه", "تاروت", "قهوه"]

# لینک عکس‌ها آنلاین
image_links = [
    f"https://katisgallery.ir/wp-content/uploads/2024/09/birth-signs-symbols-katisgallery-{i}.jpg"
    for i in range(1, 13)
]

# منوی اصلی
main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text=cat) for cat in categories]],
    resize_keyboard=True
)

# منوی ماه‌ها
def month_menu():
    kb = ReplyKeyboardBuilder()
    for month_num in months:
        kb.button(text=months[month_num])
    kb.button(text="بازگشت")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

# تولید متن فال با GPT
async def generate_horoscope(month_name: str, category: str) -> str:
    prompt = (
        f"یک فال {category} برای ماه {month_name} به زبان فارسی بنویس. "
        "حداقل 7 خط باشد و در انتها هشتگ مناسب اضافه شود."
    )
    response = await openai.ChatCompletion.acreate(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# هندلر /start
@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    await message.answer("سلام! ربات فال شما آماده است. یک دسته را انتخاب کنید:", reply_markup=main_menu)

# هندلر انتخاب دسته
@dp.message(F.text.in_(categories))
async def choose_category(message: types.Message):
    category = message.text
    await message.answer(f"حالا ماه خود را انتخاب کنید:", reply_markup=month_menu())
    message.session_data = {"category": category}

# هندلر انتخاب ماه
@dp.message(lambda m: m.text in months.values())
async def choose_month(message: types.Message):
    month_name = message.text
    category = message.session_data.get("category", "روزانه")
    month_number = list(months.keys())[list(months.values()).index(month_name)]
    image_path = image_links[month_number-1]
    horoscope = await generate_horoscope(month_name, category)
    await message.answer_photo(photo=image_path, caption=horoscope)

# بازگشت
@dp.message(F.text=="بازگشت")
async def go_back(message: types.Message):
    await message.answer("دسته را انتخاب کنید:", reply_markup=main_menu)

# اجرای ربات
async def main():
    print("🤖 ربات فال در حال اجراست...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
