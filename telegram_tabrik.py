import pandas as pd
import requests
import schedule
import time
import random
from datetime import datetime
from telegram.ext import Updater, MessageHandler, Filters

# ================== SOZLAMALAR ==================
TOKEN = "8468084793:AAGCPlKpZP8ioIziKzW5Bvz1sL-Jv20L2cg"
GROUP_ID = -1003613716463

CSV_URL = "https://docs.google.com/spreadsheets/d/14Y5SwUSgO00VTgLYAZR73XoQGg3V-p8M/export?format=csv&gid=1184571774"

rahmat_words = ["rahmat","rahmad","Rahmat","Rahmad",
                "рахмат","Рахмат","Рахмад","рахмад"]

rahmat_count = 0

random_messages = [
"🚆 Bugun yo‘llar tinch, vagonlar tartibli, siz esa fidoyi xodim sifatida o‘z ishini mukammal bajarishda davom etyapsiz! 💪",
"⚡️ Har bir temir yo‘l uzelining harakati sizning mehnatingiz bilan bog‘liq. Bugun yangi marralarga intiling! 🚄",
"🌟 Sizning mas’uliyatli mehnatingiz tufayli yurtimiz taraqqiyotga intilmoqda. Bugun ham shunday davom eting!",
"🚧 Vagonlar, relslar, stansiyalar… hammasi sizning mehnatingiz bilan tinch va xavfsiz ishlaydi. Rahmat sizga!",
"🎯 Har bir belgilangan vaqtni bajarish – bu sizning fidoyiligingiz! Bugun yangi marralarni zabt eting!",
"💡 Yangi loyihalar va imkoniyatlar – siz doimo oldindasiz!",
"🛤 Jamoamiz faol va yo‘llar xavfsiz! Sizning mehnatingiz buning garovi!",
"🌈 Har bir kun – yangi imkoniyat. Bugun ham ilhomlantiring!",
"🏅 Sizning mas’uliyatli mehnatingiz tizimni mukammal ishlashini ta’minlaydi!",
"🚀 Fidoyi xodimlar taraqqiyotga hissa qo‘shadi!"
]

# ================== TUG‘ILGAN KUN TEKSHIRISH ==================

def check_birthdays(bot):
    try:
        df = pd.read_csv(CSV_URL)
    except Exception as e:
        print("CSV yuklanmadi:", e)
        return

    today = datetime.now().strftime("%d.%m")
    birthday_people = []

    for index, row in df.iterrows():
        try:
            birth_date = str(row['tugulgan_kun'])
            name = row['ism']
            department = row['bolim']

            if today in birth_date:
                birthday_people.append((name, department))
        except:
            continue

    # ===== 1 ta xodim =====
    if len(birthday_people) == 1:
        name, dept = birthday_people[0]
        message = f"""Hurmatli {name} ({dept}) temir yo‘l sohasining fidoyi xodimi.

Sizni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!
"""
        bot.send_message(chat_id=GROUP_ID, text=message)

    # ===== 2+ ta xodim =====
    elif len(birthday_people) > 1:
        names = ", ".join([f"{n} ({d})" for n,d in birthday_people])
        message = f"""Hurmatli {names} temir yo‘l sohasining fidoyi xodimlari.

Sizlarni tug‘ilgan kuningiz bilan chin qalbimizdan tabriklaymiz. Mas’uliyatli va sharafli mehnatingiz bilan yurtimiz taraqqiyotiga munosib hissa qo‘shib kelmoqdasiz. Sizlarga mustahkam sog‘liq, oilaviy baxt, ishlaringizda doimiy muvaffaqiyat va xavfsiz yo‘llar tilaymiz! Yana bir bor tug'ulgan kunigiz bilan tabriklaymiz.

Hurmat bilan "Qo'qon elektr ta'minoti" masofasi filiali!
"""
        bot.send_message(chat_id=GROUP_ID, text=message)

    # ===== Tug‘ilgan kun yo‘q =====
    else:
        main_msg = "🎉 Afsus! Bugun tug‘ilgan kun yo‘q! Lekin bugun mening tug‘ilgan kunim! Uraaa, tabriklasalaring bo‘ladi! 🥳🎂"
        bot.send_message(chat_id=GROUP_ID, text=main_msg)

        random_msg = "Afsus! Bugun tug‘ilgan kun yo‘q!\n\n" + random.choice(random_messages)
        bot.send_message(chat_id=GROUP_ID, text=random_msg)


# ================== RAHMAT JAVOB ==================

def reply_handler(update, context):
    global rahmat_count
    text = update.message.text

    if text in rahmat_words:
        rahmat_count += 1

        if rahmat_count == 1:
            update.message.reply_text("🤗 Sizga doimo muvaffaqiyat tilaymiz!")
        elif rahmat_count >= 2:
            update.message.reply_text("😅 qaytarormen maazgii")
            rahmat_count = 0


# ================== BOT ISHGA TUSHISH ==================

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))

    schedule.every().day.at("09:00").do(lambda: check_birthdays(updater.bot))

    updater.start_polling()

    while True:
        schedule.run_pending()
        time.sleep(10)


if __name__ == "__main__":
    main()
