from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import TELEGRAM_BOT_TOKEN
from weather import get_weather

# Стан користувачів
user_state = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я бот для погоди. "
                                    "Використай /help щоб дізнатися більше.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – привітання\n"
        "/help – список команд\n"
        "/weather – отримати погоду у вибраному місті"
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_state[user_id] = "waiting_city"
    await update.message.reply_text("Вкажіть місто:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_state.get(user_id) == "waiting_city":
        city = update.message.text
        result = get_weather(city)
        await update.message.reply_text(result)
        user_state[user_id] = None

def run_bot():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                                   handle_message))

    print("Бот запущено...")
    app.run_polling()
