from telegram.ext import ApplicationBuilder, MessageHandler, filters
import os
import pandas as pd
import asyncio
from datetime import datetime
import random

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
        df = pd.read_csv(SHEET_CSV).fillna('')
        df['tugilgan_kun'] = pd.to_datetime(df['tugilgan_kun'], errors='coerce')
        today = datetime.now()
        return df[(df['tugilgan_kun'].dt.day == today.day) &
                  (df['tugilgan_kun'].dt.month == today.month)]
    except Exception as e:
        print("Xatolik CSV faylni o‘qishda:", e)
        return pd.DataFrame()

# --- Tug‘ilgan kun xabarini yuborish ---
async def send_birthday_message(app):
    df = get_today_birthdays()
    if df.empty:
        msg = random.choice(MOTIVATION_MESSAGES)
    else:
        names = [f"*{row['ism']} ({row['bolim']})*" if row.get('bolim') else f"*{row['ism']}*"
                 for _, row in df.iterrows() if row.get('ism')]
        if len(names) == 1:
            msg = f"🎉 Hurmatli {names[0]}, sizni tug‘ilgan kuningiz bilan tabriklaymiz! Mas’uliyatli mehnatingiz uchun rahmat!"
        else:
            msg = f"🎉 Hurmatli {', '.join(names)}, sizni tug‘ilgan kuningiz bilan tabriklaymiz! Mas’uliyatli mehnatingiz uchun rahmat!"
    try:
        await app.bot.send_message(chat_id=GROUP_ID, text=msg, parse_mode="Markdown")
    except Exception as e:
        print("Xatolik Telegramga yuborishda:", e)

# --- Rahmat xabarlariga javob ---
async def handle_thanks(update, context):
    user_id = update.effective_user.id
    count = THANKS_COUNTER.get(user_id, 0) + 1
    THANKS_COUNTER[user_id] = count
    reply = "🤗 Sizga doimo salomatlik va muvaffaqiyat tilaymiz!" if count == 1 else "😅 Qaytarormen! maazgii"
    await update.message.reply_text(reply)

# --- Botni ishga tushirish ---
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Rahmat xabarlarini tinglash
    thanks_words = ["rahmat", "raxmat", "raxmad", "rahmad", "рахмад", "рамат"]
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("|".join(thanks_words)), handle_thanks))

    # Tug‘ilgan kun xabarini yuborish
    await send_birthday_message(app)

    # Botni ishga tushirish
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    asyncio.run(main())
