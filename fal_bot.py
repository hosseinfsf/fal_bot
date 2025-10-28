import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from utils.keyboards import main_menu, zodiac_menu, donate_menu
from utils.horoscope_ai import generate_horoscope
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_category = {}

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "✨ به ربات فال‌گو خوش اومدی!\n\nیکی از گزینه‌های زیر رو انتخاب کن 👇",
        reply_markup=main_menu()
    )

@dp.callback_query(F.data.in_({"daily","weekly","monthly","love","coffee","tarot"}))
async def choose_category(callback: types.CallbackQuery):
    user_category[callback.from_user.id] = callback.data
    await callback.message.edit_text("ماه تولدت رو انتخاب کن 🌙", reply_markup=zodiac_menu())

@dp.callback_query(F.data.startswith("sign_"))
async def show_horoscope(callback: types.CallbackQuery):
    sign = callback.data.replace("sign_", "")
    category = user_category.get(callback.from_user.id, "daily")

    await callback.message.edit_text("🔮 در حال نوشتن فال مخصوص تو... ⏳")

    text = await generate_horoscope(sign, category)
    await callback.message.edit_text(
        f"✨ {sign} - {category.upper()} ✨\n\n{text}",
        reply_markup=donate_menu()
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
