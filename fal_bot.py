# fal_bot.py
import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import openai

# وب‌سرور
from aiohttp import web

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_KEY = os.getenv("OPENAI_KEY")
DONATE_LINK = os.getenv("DONATE_LINK", "")

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN not set in .env")
if not OPENAI_KEY:
    raise RuntimeError("OPENAI_KEY not set in .env")

openai.api_key = OPENAI_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ماه‌ها ساده
months = [
    "فروردین","اردیبهشت","خرداد",
    "تیر","مرداد","شهریور",
    "مهر","آبان","آذر",
    "دی","بهمن","اسفند"
]

categories = ["روزانه","هفتگی","ماهانه","عشق","قهوه","تاروت"]

# منوی ساده
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[[types.KeyboardButton(text=cat) for cat in categories[i:i+3]] for i in range(0, len(categories), 3)],
        resize_keyboard=True
    )
    await message.answer("سلام! یک دسته را انتخاب کنید:", reply_markup=keyboard)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await cmd_start(message)

# انتخاب دسته
@dp.message(lambda m: m.text in categories)
async def choose_category(message: types.Message):
    # ذخیره دسته در session ساده (این روش محدود هست؛ برای پرو덕شن از FSM استفاده کن)
    message.chat_data = getattr(message, "chat_data", {})
    message.chat_data["category"] = message.text
    # منوی ماه‌ها
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(0, 12, 3):
        kb.row(*[types.KeyboardButton(months[j]) for j in range(i, i+3)])
    kb.add(types.KeyboardButton(text="بازگشت"))
    await message.answer("ماه تولد را انتخاب کنید:", reply_markup=kb)

# تولید فال از OpenAI (نمونه ساده)
async def generate_horoscope(month_name: str, category: str) -> str:
    prompt = (
        f"یک فال {category} برای ماه {month_name} به زبان فارسی بنویس. "
        "حداقل 7 خط، شامل ایموجی و 2-4 هشتگ و لحن مثبت و شاعرانه."
    )
    try:
        resp = await openai.ChatCompletion.acreate(
            model="gpt-4o-mini",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            max_tokens=450
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        # بازگشت متن جایگزین در صورت خطا
        return f"⚠️ خطا در دریافت فال از سرویس هوش‌مصنوعی.\nاین یک فال پیش‌فرض برای {month_name} است.\n\n🌟 امروز فرصتی برای شروع دوباره داری...\n#فال #آغاز"

# انتخاب ماه و ارسال فال
@dp.message(lambda m: m.text in months)
async def choose_month(message: types.Message):
    month = message.text
    # تلاش برای پیدا کردن category ذخیره شده؛ اگر نبود روزانه در نظر گرفته میشه
    category = getattr(message, "chat_data", {}).get("category", "روزانه")
    await message.answer("در حال آماده‌سازی فال... ⏳")
    text = await generate_horoscope(month, category)
    # ارسال عکس آنلاین (در صورت نیاز)
    # لینک های نمونه:
    image_links = [
        f"https://katisgallery.ir/wp-content/uploads/2024/09/birth-signs-symbols-katisgallery-{i}.jpg"
        for i in range(1,13)
    ]
    idx = months.index(month)
    photo = image_links[idx]
    # دکمه Donate
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton(text="💎 حمایت با کریپتو"))
    await message.answer_photo(photo=photo, caption=text, reply_markup=kb)

@dp.message(lambda m: m.text == "بازگشت")
async def back(message: types.Message):
    await cmd_start(message)

@dp.message(lambda m: m.text == "💎 حمایت با کریپتو")
async def donate_handler(message: types.Message):
    link = DONATE_LINK or "https://your-crypto-link.com"
    await message.answer(f"برای حمایت، این لینک را استفاده کنید:\n{link}")

# ---- وب‌سرور خیلی ساده برای health check ----
async def handle_root(request):
    return web.Response(text="OK")

async def start_aiohttp_server():
    app = web.Application()
    app.router.add_get("/", handle_root)
    port = int(os.getenv("PORT", "10000"))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Health server started on port {port}")

# ---- main: اجرا همزمان وب‌سرور و polling ----
async def main():
    # استارت وب‌سرور
    await start_aiohttp_server()
    # استارت polling
    print("Starting bot polling...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
