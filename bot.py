import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# --- Логирование ---
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tg-bot")

# --- Переменные окружения ---
TOKEN = os.getenv("TOKEN")  # задай в Render -> Environment
PORT = int(os.getenv("PORT", "8080"))  # Render задаёт сам
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("WEBHOOK_URL")  # публичный URL сервиса

# --- Хэндлеры ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот на Render + вебхуки готов 🚀")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Команды: /start, /help — и я эхо-бот для текста.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        await update.message.reply_text(update.message.text)

# --- Точка входа ---
def main():
    if not TOKEN:
        raise RuntimeError("Нет TOKEN в переменных окружения")

    if not BASE_URL:
        raise RuntimeError("Нет RENDER_EXTERNAL_URL/WEBHOOK_URL — Render ещё не выдал публичный URL")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Уникальный путь вебхука — используем токен в пути
    webhook_url = f"{BASE_URL.rstrip('/')}/{TOKEN}"

    log.info("Starting webhook on port %s", PORT)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        drop_pending_updates=True,  # не обрабатывать старые накопившиеся апдейты
    )

if __name__ == "__main__":
    main()
