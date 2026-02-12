import pandas as pd
import asyncio
import random
from datetime import datetime
from telegram import Bot, Update
from telegram.ext import ContextTypes
import os

# --- Sozlamalar ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = -1003613716463
SHEET_CSV = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv&gid=1184571774"

# --- Motivatsion xabarlar ---
MOTIVATION_MESSAGES = [
    "🚆 Bugun yo‘llar tinch, vagonlar tartibli, siz esa fidoyi xodim sifatida o‘z ishini mukammal bajarishda davom etyapsiz! 💪",
    "⚡️ Har bir temir yo‘l uzelining harakati sizning mehnatingiz bilan bog‘liq. Bugun yangi marralarga intiling! 🚄",
    "🌟 Sizning mas’uliyatli va e’tiborli mehnatingiz tufayli yurtimiz taraqqiyotga intilmoqda. Bugun ham shunday davom eting!",
    "🚧 Vagonlar, relslar, stansiyalar… hammasi sizning mehnatingiz bilan tinch va xavfsiz ishlaydi. Rahmat sizga!",
    "🎯 Har bir to‘xtovsiz harakat, har bir belgilangan vaqtni bajarish – bu sizning fidoyiligingiz! Bugun yangi marralarni zabt eting!",
    "💡 Yangi loyihalar, yangi imkoniyatlar – temir yo‘l sohasi doimo yangilanadi. Siz ham yangilikka tayyormisiz?",
    "🛤 Bugun hech kim tug‘ilgan kunini nishonlamasa ham, jamoamiz faol va yo‘llar xavfsiz! Sizning mehnatingiz buning garovi!",
    "🌈 Har bir kun – yangi imkoniyat. Bugun biror yangilikni o‘zingiz yaratib, hamkasblaringizni ilhomlantiring!",
    "🏅 Sizning mas’uliyatli mehnatingiz temir yo‘l infratuzilmasini mukammal ishlashini ta’minlaydi. Bugun ham shunday davom eting!",
    "🚀 Fidoyi xodimlar yo‘llarimizni xavfsiz qiladi va taraqqiyotga hissa qo‘shadi. Bugun yangi marralarga intiling!"
]

# --- Rahmat xabarlarini hisoblash ---
THANKS_COUNTER = {}

# --- Bugungi tug‘ilgan kunlarni olish ---
def get_today_birthdays():
    try:
        df = pd.read_csv(SHEET_CSV)
        df = df.fillna('')
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) &
                  (df['tugilgan_kun'].dt.month == today.month)]
    except Exception as e:
        print("Xatolik CSV faylni o‘qishda:", e)
        return pd.DataFrame()

# --- Xabar tayyorlash ---
def prepare_message(df):
    if df.empty:
        return "Afsus, bugun tug‘ilgan kun yo‘q!\n\n" + random.choice(MOTIVATION_MESSAGES)

    names = []
    for _, row in df.iterrows():
        ism = str(row.get('ism', '')).strip()
        bolim = str(row.get('bolim', '')).strip()
        if ism:
            names.append(f"*{ism} ({bolim})*" if bolim else f"*{ism}*")

    if len(names) == 1:
        return f"""Hurmatli {names[0]} temir yo‘l sohasining fidoyi xodimi.

Sizni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!"""
    else:
        return f"""Hurmatli {', '.join(names)} temir yo‘l sohasining fidoyi xodimlari.

Sizlarni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizlarga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!"""
# --- Telegramga xabar yuborish ---
async def send_message(text):
    try:
        bot = Bot(BOT_TOKEN)
        await bot.send_message(chat_id=GROUP_ID, text=text, parse_mode="Markdown")
    except Exception as e:
        print("Xatolik Telegramga yuborishda:", e)
# --- Rahmatga javob berish ---
async def handle_thanks(user_id: int, update: Update):
    count = THANKS_COUNTER.get(user_id, 0) + 1
    THANKS_COUNTER[user_id] = count
    if count == 1:
        await update.message.reply_text("🤗 Sizga doimo salomatlik va muvaffaqiyat tilaymiz!")
    else:
        await update.message.reply_text("😅 Qaytarormen!")

# --- Foydalanuvchi xabarlarini tekshirish ---
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    thanks_words = ["rahmat", "raxmat", "raxmad", "rahmad", "рахмад", "рамат"]
    text = update.message.text.lower()
    if any(word in text for word in thanks_words):
        await handle_thanks(update.message.from_user.id, update)

# --- Botni ishga tushirish ---
async def main():
    df = get_today_birthdays()
    msg = prepare_message(df)
    if msg:
        await send_message(msg)

if __name__ == "__main__":
    asyncio.run(main())
