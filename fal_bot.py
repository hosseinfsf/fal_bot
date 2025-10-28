import os
import openai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiohttp import web
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PORT = int(os.environ.get("PORT", 8000))
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

openai.api_key = OPENAI_API_KEY
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# کیبورد اصلی
keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton("فال امروز 🌞", callback_data="daily")],
    [InlineKeyboardButton("فال هفتگی 🔮", callback_data="weekly")],
    [InlineKeyboardButton("فال ماهانه 🌙", callback_data="monthly")],
    [InlineKeyboardButton("💰 Donate", url="https://YOUR_CRYPTO_OR_PAYPAL_LINK")]
])

async def generate_horoscope(horoscope_type: str, month: int):
    prompt = f"یک فال {horoscope_type} برای ماه {month} به فارسی با حداقل ۷ خط، emoji و هشتگ بساز."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

@dp.message(commands=["start"])
async def start(msg: types.Message):
    # کلید انتخاب ماه
    month_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(str(i), callback_data=f"month_{i}") for i in range(1, 4)],
        [InlineKeyboardButton(str(i), callback_data=f"month_{i}") for i in range(4, 7)],
        [InlineKeyboardButton(str(i), callback_data=f"month_{i}") for i in range(7, 10)],
        [InlineKeyboardButton(str(i), callback_data=f"month_{i}") for i in range(10, 13)],
    ])
    await msg.answer("سلام! ماه تولدتو انتخاب کن 🌟", reply_markup=month_keyboard)

# دریافت ماه
@dp.callback_query(Text(startswith="month_"))
async def month_selected(query: types.CallbackQuery):
    month = int(query.data.split("_")[1])
    await query.message.answer(f"ماه {month} انتخاب شد! حالا فال مورد نظر رو انتخاب کن:", reply_markup=keyboard)
    await query.answer()

# فال روزانه
@dp.callback_query(Text("daily"))
async def daily(query: types.CallbackQuery):
    text = await generate_horoscope("روزانه", month=1)  # می‌تونیم ماه رو ذخیره کنیم
    await query.message.answer(text)
    await query.answer()

# فال هفتگی
@dp.callback_query(Text("weekly"))
async def weekly(query: types.CallbackQuery):
    text = await generate_horoscope("هفتگی", month=1)
    await query.message.answer(text)
    await query.answer()

# فال ماهانه
@dp.callback_query(Text("monthly"))
async def monthly(query: types.CallbackQuery):
    text = await generate_horoscope("ماهانه", month=1)
    await query.message.answer(text)
    await query.answer()

# Webhook
async def handle(request):
    data = await request.json()
    update = types.Update(**data)
    await dp.process_update(update)
    return web.Response()

app = web.Application()
app.router.add_post(f"/{BOT_TOKEN}", handle)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=PORT)
