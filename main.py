from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام خوبی؟ 😊")

if __name__ == '__main__':
    TOKEN = "7831184685:AAGYVXKQ1lorzH9XmoosYtv8s07F1ioqCQo"
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
