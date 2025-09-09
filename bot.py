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

# ====== РЕДАКТИРУЕМЫЕ НАДПИСИ / ТЕКСТЫ ======
# Подписи кнопок стартового меню (изменяйте смело)
MAIN_MENU_LABELS = {
    "btn1": "Кнопка 1 (подменю)",
    "btn2": "Кнопка 2",
    "btn3": "Кнопка 3",
    "btn4": "Кнопка 4",
}

# Текстовые ответы для кнопок 2–4 стартового меню
MAIN_MENU_TEXTS = {
    "btn2": "Содержимое для Кнопки 2.",
    "btn3": "Содержимое для Кнопки 3.",
    "btn4": "Содержимое для Кнопки 4.",
}

# Подписи кнопок в подменю Кнопки 1
SUB1_MENU_LABELS = {
    "sub1_a": "Подменю 1 → Пункт A",
    "sub1_b": "Подменю 1 → Пункт B",
    "back_main": "⬅ Назад",
}

# Текстовые ответы пунктов подменю 1
SUB1_TEXTS = {
    "sub1_a": "Выбрали Подменю 1 / Пункт A.",
    "sub1_b": "Выбрали Подменю 1 / Пункт B.",
}

# ====== КЛАВИАТУРЫ ======
def build_main_menu():
    """Главное меню (4 кнопки)."""
    kb = [
        [InlineKeyboardButton(MAIN_MENU_LABELS["btn1"], callback_data="btn1")],
        [InlineKeyboardButton(MAIN_MENU_LABELS["btn2"], callback_data="btn2")],
        [InlineKeyboardButton(MAIN_MENU_LABELS["btn3"], callback_data="btn3")],
        [InlineKeyboardButton(MAIN_MENU_LABELS["btn4"], callback_data="btn4")],
    ]
    return InlineKeyboardMarkup(kb)

def build_submenu1():
    """Подменю для кнопки 1."""
    kb = [
        [InlineKeyboardButton(SUB1_MENU_LABELS["sub1_a"], callback_data="sub1_a")],
        [InlineKeyboardButton(SUB1_MENU_LABELS["sub1_b"], callback_data="sub1_b")],
        [InlineKeyboardButton(SUB1_MENU_LABELS["back_main"], callback_data="back_main")],
    ]
    return InlineKeyboardMarkup(kb)

# ====== ХЭНДЛЕРЫ ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Главное меню:", reply_markup=build_main_menu())

async def on_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()

    cd = q.data

    # Ветвление: Кнопка 1 открывает подменю
    if cd == "btn1":
        await q.message.edit_text("Подменю 1:", reply_markup=build_submenu1())
        return

    # Обработка подменю 1
    if cd in ("sub1_a", "sub1_b"):
        text = SUB1_TEXTS.get(cd, "Неизвестный пункт подменю.")
        # Оставляем в подменю, можно легко поменять на возврат в главное
        await q.message.edit_text(f"{text}\n\nОстаться в подменю 1 или вернуться назад:",
                                  reply_markup=build_submenu1())
        return

    if cd == "back_main":
        await q.message.edit_text("Главное меню:", reply_markup=build_main_menu())
        return

    # Кнопки 2–4 стартового меню просто показывают текст и возвращают в главное меню
    if cd in ("btn2", "btn3", "btn4"):
        text = MAIN_MENU_TEXTS.get(cd, "Содержимое не задано.")
        await q.message.edit_text(f"{text}\n\nВозврат в меню:", reply_markup=build_main_menu())
        return

    # Фоллбек
    await q.message.edit_text("Неизвестная команда. Возврат в меню:", reply_markup=build_main_menu())

# ====== ЗАПУСК ======
def main():
    if not TOKEN:
        raise RuntimeError("Нет TOKEN в переменных окружения")
    if not BASE_URL:
        raise RuntimeError("Нет публичного URL (RENDER_EXTERNAL_URL/WEBHOOK_URL)")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(on_click))

    webhook_url = BASE_URL  # слушаем КОРЕНЬ (PTB v20 run_webhook хэндлит /)
    log.info("Starting webhook on %s (port %s)", webhook_url, PORT)

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=webhook_url,
        drop_pending_updates=True,
    )

if __name__ == "__main__":
    main()
