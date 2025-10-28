import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from datetime import date
import random

# 🔹 توکن ربات تلگرام خودت رو اینجا بذار
TOKEN = "8433493630:AAGpK1f36gI7Rs22f8F0k2pLRpx9QZv10wg"

# 🔹 مسیر عکس‌ها (که از 1.jpg تا 12.jpg نام‌گذاری شدن)
IMAGE_PATH = "images"

# 🔹 لیست فال‌های هر ماه (می‌تونی بعداً قشنگ‌ترش کنی)
HOROSCOPES = {
    1: "امروز روزی پر از انرژی و فرصت‌های تازه‌ست.",
    2: "کمی صبور باش، نتیجه تلاش‌هات نزدیکه.",
    3: "ممکنه از جایی که انتظار نداری خوشحال شی.",
    4: "به حس درونیت اعتماد کن، راه رو نشونت میده.",
    5: "یه تصمیم مهم جلوته، قبل از اقدام فکر کن.",
    6: "امروز وقت استراحته، به خودت فرصت بده.",
    7: "یک پیام یا خبر خوب در راهه!",
    8: "دلسوزی تو باعث میشه اطرافیانت بهت نزدیک‌تر بشن.",
    9: "در کارها عجله نکن، آرامش کلیده موفقیته.",
    10: "با برنامه پیش برو، موفقیت حتمیه.",
    11: "یه نفر داره از دور حواسش بهته 😉",
    12: "زمان برای شروع یه کار جدید عالیه!"
}

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔹 شروع ربات
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    text = "سلام! 🌟\nماه تولدت رو انتخاب کن تا فال امروزت رو ببینی 👇"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text=f"ماه {i}")] for i in range(1, 13)
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard)

# 🔹 وقتی ماه انتخاب میشه
@dp.message()
async def send_horoscope(message: types.Message):
    try:
        month = int(message.text.replace("ماه ", ""))
        horoscope = HOROSCOPES.get(month, "ماه وارد شده اشتباهه!")
        image_path = f"{IMAGE_PATH}/{month}.jpg"
        await message.answer_photo(photo=open(image_path, "rb"), caption=f"✨ فال امروز:\n\n{horoscope}")
    except Exception as e:
        await message.answer("یه مشکلی پیش اومد. لطفاً دوباره امتحان کن 🌙")

async def main():
    print("🤖 ربات فال روزانه در حال اجراست...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
