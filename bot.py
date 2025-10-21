import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
import os

# Tokenni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name

    keyboard = [[KeyboardButton("/start")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        f"Assalomu Alaykum, {user}! 👋\n\n"
        "Man uch tilda tarjima qiluvchi botman 🇺🇿 🇷🇺 🇬🇧.\n"
        "So‘z yoki gap jo'nating — man uni o‘zbek, rus va ingliz tillariga tarjima qilib beraman."
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
            f"🌍 Sorov natijasi:\n{text}\n\n"
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

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    print("✅ Bot ishlavoti...")
    app.run_polling()

if __name__ == "__main__":
    main()
