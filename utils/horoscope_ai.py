from openai import OpenAI
import random

client = OpenAI()

async def generate_horoscope(sign: str, category: str):
    """تولید فال هوشمند با GPT یا بازگشت متن آماده"""
    topics = {
        "daily": "فال روزانه",
        "weekly": "فال هفتگی",
        "monthly": "فال ماهانه",
        "love": "فال عشق",
        "coffee": "فال قهوه",
        "tarot": "فال تاروت",
    }

    prompt = f"""
    تو یک نویسنده فال حرفه‌ای و شاعرانه هستی.
    برای {topics.get(category, 'فال')} مخصوص ماه {sign} بنویس.
    فال باید حداقل ۷ خط باشد، شامل ایموجی، هشتگ و لحن مثبت و پرانرژی باشد.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=400,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        from utils.texts import fallback_horoscope
        return fallback_horoscope(sign, category)
