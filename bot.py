import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from flask import Flask, request
import os

# Muhitdan tokenni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Flask ilovasi
app = Flask(__name__)

# Logging sozlamasi
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Telegram bot ilovasi
application = ApplicationBuilder().token(BOT_TOKEN).build()

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    keyboard = [[KeyboardButton("/start")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        f"Assalomu alaykum, {user}! 👋\n\n"
        "Man to'rt tilda tarjima qiluvchi botman 🇺🇿 🇷🇺 🇬🇧.\n"
        "So‘z yoki gap jo'nating — man uni o‘zbek, rus, ingliz va turk tillariga tarjima qilib beraman.",
        reply_markup=reply_markup
    )

# Tarjima funksiyasi
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    try:
        uzb = GoogleTranslator(source='auto', target='uz').translate(text)
        eng = GoogleTranslator(source='auto', target='en').translate(text)
        ru = GoogleTranslator(source='auto', target='ru').translate(text)
        tr = GoogleTranslator(source='auto', target='tr').translate(text)

        response = (
            f"🌍 So‘rov natijasi:\n{text}\n\n"
            f"🇺🇿 O‘zbekcha: {uzb}\n"
            f"🇬🇧 Inglizcha: {eng}\n"
            f"🇷🇺 Ruscha: {ru}\n"
            f"🇹🇷 Turkcha: {tr}"
        )

        keyboard = [[KeyboardButton("/start")]]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(response, reply_markup=reply_markup)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Xatolik yuz berdi, qayta urinib ko‘ring.")

# Handlerlar
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

# Flask endpoint (Telegram webhook chaqiradi)
@app.post(f"/{BOT_TOKEN}")
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

# Flask serverni ishga tushirish
if __name__ == "__main__":
    print(" Flask + Telegram bot server ishga tushdi...")
    app.run(host="0.0.0.0", port=8000)
