from deep_translator import GoogleTranslator
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
import os
from dotenv import load_dotenv
import logging
import tempfile

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
        f"👋 Assalomu alaykum, Botimizga xush kelibsiz {user}!\n\n"
        "Man ko‘p tillarga tarjima qiluvchi botman 🌍.\n"
        "So‘z yoki gap yuboring — man uni quyidagi tillarga tarjima qilib, matn va ovoz shaklida qaytaraman:\n\n"
        "🇺🇿 O‘zbekcha\n"
        "🇬🇧 Inglizcha\n"
        "🇷🇺 Ruscha\n"
        "🇹🇷 Turkcha\n"
        "🇩🇪 Nemischa\n"
        "🇰🇷 Koreyscha\n"
        "🇸🇦 Arabcha\n\n"
        "Iltimos, tarjima qilinadigan so‘z yoki gapni jo'nating✍️",
        reply_markup=reply_markup
    )

# Tarjima va ovoz qaytarish funksiyasi
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    languages = {
        "🇺🇿 O‘zbekcha": "uz",
        "🇬🇧 Inglizcha": "en",
        "🇷🇺 Ruscha": "ru",
        "🇹🇷 Turkcha": "tr",
        "🇩🇪 Nemischa": "de",
        "🇰🇷 Koreyscha": "ko",
        "🇸🇦 Arabcha": "ar"
    }

    try:
        response = f"🌍 So‘rov natijasi:\n\n{text}\n\n"
        for lang_name, lang_code in languages.items():
            # Tarjima
            translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
            response += f"{lang_name}: {translated}\n"

            # Ovoz yaratish (gTTS yordamida)
            try:
                tts = gTTS(translated, lang=lang_code)
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tts.save(tmp_file.name)
                    await update.message.reply_voice(
                        voice=open(tmp_file.name, "rb"),
                        caption=f"{lang_name} ovozli tarjima 🎧"
                    )
                    os.remove(tmp_file.name)
            except Exception as e:
                print(f"Ovoz hosil qilishda xatolik ({lang_code}):", e)

        await update.message.reply_text(response)

    except Exception as e:
        print("Xatolik:", e)
        await update.message.reply_text("❌ Tarjima vaqtida xatolik yuz berdi, qayta urinib ko‘ring.")

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))
    print("✅ Bot ishlavoti...")
    app.run_polling()

if __name__ == "__main__":
    main()
