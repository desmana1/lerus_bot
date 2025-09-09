import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes
)

# Логирование
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("tg-bot")

# Читаем токен из переменных окружения
TOKEN = os.getenv("TOKEN")
PORT = int(os.getenv("PORT", "8080"))
BASE_URL = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("WEBHOOK_URL")


# --- Хэндлеры ---

def main_menu():
    """Главное меню (4 кнопки)."""
    keyboard = [
        [InlineKeyboardButton("📌 Информация 1", callback_data="info1")],
        [InlineKeyboardButton("📌 Информация 2", callback_data="info2")],
        [InlineKeyboardButton("📌 Информация 3", callback_data="info3")],
        [InlineKeyboardButton("📌 Информация 4", callback_data="info4")],
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    await update.message.reply_text("Главное меню:", reply_markup=main_menu())


async def on_menu_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка нажатий кнопок меню"""
    query = update.callback_query
    await query.answer()

    if query.data == "info1":
        text = "Это текстовый блок №1. Здесь может быть любая справочная информация."
    elif query.data == "info2":
        text = "Это текстовый блок №2. Например, описание сервиса или продукта."
    elif query.data == "info3":
        text = "Это текстовый блок №3. Здесь можно вставить инструкцию или ссылку."
    elif query.data == "info4":
        text = "Это текстовый блок №4. Дополнительные сведения."
    else:
        text = "Неизвестный пункт."

    await query.message.edit_text(f"{text}\n\nВозврат в меню:", reply_markup=main_menu())


# --- Запуск ---

def main():
    if not TOKEN:
        raise RuntimeError("Нет TOKEN в переменных окружения")

    if not BASE_URL:
        raise RuntimeError("Нет RENDER_EXTERNAL_URL/WEBHOOK_URL")

    app = Application.builder().token(TOKEN).build()

    # Команды и кнопки
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_menu_click))

    # Webhook для Render
    webhook_url = f"{BASE_URL.rstrip('/')}/{TOKEN}"
    log.info("Starting webhook on %s", webhook_url)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
