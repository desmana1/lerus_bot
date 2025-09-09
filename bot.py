import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Логи ---
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tg-bot")

# --- ENV ---
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = (os.getenv("RENDER_EXTERNAL_URL") or os.getenv("WEBHOOK_URL") or "").rstrip("/")

# --- UI ---
def build_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton("Кнопка 2", callback_data="btn2")],
        [InlineKeyboardButton("Кнопка 3", callback_data="btn3")],
        [InlineKeyboardButton("Кнопка 4", callback_data="btn4")],
    ])

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню:", reply_markup=build_menu())

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    mapping = {
        "btn1": "Вы нажали кнопку 1",
        "btn2": "Вы нажали кнопку 2",
        "btn3": "Вы нажали кнопку 3",
        "btn4": "Вы нажали кнопку 4",
    }
    text = mapping.get(q.data, "Неизвестная кнопка")
    await q.message.edit_text(f"{text}\n\nВозврат в меню:", reply_markup=build_menu())

# --- Entry point ---
def main():
    if not TOKEN:
        raise RuntimeError("Нет TOKEN в переменных окружения")
    if not BASE_URL:
        raise RuntimeError("Нет публичного URL (RENDER_EXTERNAL_URL/WEBHOOK_URL)")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_click))

    # В PTB v20 run_webhook сам поставит вебхук на указанный URL
    webhook_url = BASE_URL  # слушаем КОРЕНЬ, без /telegram-webhook
    log.info("Starting webhook on %s (port %s)", webhook_url, PORT)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
