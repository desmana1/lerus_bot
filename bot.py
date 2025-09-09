import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")  # токен из Render → Environment
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("WEBHOOK_URL")

def build_menu():
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data="btn1")],
        [InlineKeyboardButton("Кнопка 2", callback_data="btn2")],
        [InlineKeyboardButton("Кнопка 3", callback_data="btn3")],
        [InlineKeyboardButton("Кнопка 4", callback_data="btn4")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню:", reply_markup=build_menu())

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    texts = {
        "btn1": "Вы нажали кнопку 1",
        "btn2": "Вы нажали кнопку 2",
        "btn3": "Вы нажали кнопку 3",
        "btn4": "Вы нажали кнопку 4",
    }
    text = texts.get(q.data, "Неизвестная кнопка")

    await q.message.edit_text(f"{text}\n\nВозврат в меню:", reply_markup=build_menu())

def main():
    if not TOKEN or not BASE_URL:
        raise RuntimeError("Нет TOKEN или RENDER_EXTERNAL_URL")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_click))

    webhook_url = f"{BASE_URL.rstrip('/')}/telegram-webhook"  # безопасный путь
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
