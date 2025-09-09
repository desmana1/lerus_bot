from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8254016879:AAG357kGbNnw3RoAeF7Z8M6_UqBr0fBi-7A"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я твой бот.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
