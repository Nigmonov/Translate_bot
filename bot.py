import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

# 🔹 .env fayldan tokenni yuklash
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# 🔹 Logging sozlamasi
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# 🔹 /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Assalomu alaykum, {user}!\n\n"
        "Men ko‘p tilli tarjimon botman 🌍.\n"
        "Quyidagi tillar orasida tarjima qila olaman:\n"
        "🇺🇿 O‘zbek tili\n"
        "🇷🇺 Rus tili\n"
        "🇬🇧 Ingliz tili\n"
        "🇹🇷 Turk tili\n\n"
        "Iltimos, tarjima qilinadigan so‘z yoki gapni yuboring ✍️"
    )

# 🔹 Tarjima funksiyasi
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        uzb = GoogleTranslator(source='auto', target='uz').translate(text)
        eng = GoogleTranslator(source='auto', target='en').translate(text)
        ru = GoogleTranslator(source='auto', target='ru').translate(text)
        tr = GoogleTranslator(source='auto', target='tr').translate(text)

        response = (
            f"🌍 Asl matn: {text}\n\n"
            f"🇺🇿 O‘zbekcha: {uzb}\n"
            f"🇬🇧 Inglizcha: {eng}\n"
            f"🇷🇺 Ruscha: {ru}\n"
            f"🇹🇷 Turkcha: {tr}"
        )

        await update.message.reply_text(response)

    except Exception as e:
        logging.error(f"Tarjima xatoligi: {e}")
        await update.message.reply_text("❌ Tarjima qilishda xatolik yuz berdi, qayta urinib ko‘ring.")

# 🔹 Asosiy funksiya
def main():
    if not BOT_TOKEN:
        raise ValueError("❗ BOT_TOKEN topilmadi. Iltimos, .env faylga tokenni kiriting yoki Render’da environment variable qo‘shing.")

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Buyruqlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    print("✅ Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
