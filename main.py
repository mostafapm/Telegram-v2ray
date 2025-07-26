from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

TOKEN = os.environ.get("TOKEN")  # توکن را در محیط render تعریف کن

# لیست کانفیگ‌ها (می‌تونه از فایل یا دیتابیس هم بیاد)
configs = {
    "کانفیگ v2ray 🇺🇸": "vless://uuid@ip:port?security=tls&type=ws#USA",
    "کانفیگ v2ray 🇩🇪": "vless://uuid@ip:port?security=tls&type=ws#Germany",
    "کانفیگ v2ray 🇸🇬": "vless://uuid@ip:port?security=tls&type=ws#Singapore",
}

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)] for name in configs
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سلام 👋\nیکی از کانفیگ‌ها رو انتخاب کن:", reply_markup=reply_markup
    )

# هندل انتخاب کانفیگ
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    selected = query.data
    config = configs.get(selected, "کانفیگ پیدا نشد.")
    await query.message.reply_text(f"🔐 کانفیگ مورد نظر:\n\n`{config}`", parse_mode="Markdown")

# اجرای برنامه
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ ربات در حال اجراست...")
    app.run_polling()
