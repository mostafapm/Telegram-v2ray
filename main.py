import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# لیست کانفیگ‌ها
configs = {
    "🇺🇸 کانفیگ آمریکا": "vless://uuid@us.example.com:443?security=tls&type=ws#USA",
    "🇩🇪 کانفیگ آلمان": "vless://uuid@de.example.com:443?security=tls&type=ws#Germany"
}

# پاسخ به /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in configs]
    await update.message.reply_text("سلام، یکی از کانفیگ‌ها رو انتخاب کن:", reply_markup=InlineKeyboardMarkup(keyboard))

# وقتی روی دکمه کلیک شد
async def handle_config_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    name = query.data
    config = configs.get(name, "کانفیگ پیدا نشد.")
    await query.message.reply_text(f"`{config}`", parse_mode="Markdown")

# اجرای اصلی
if __name__ == '__main__':
    TOKEN = os.environ.get("TOKEN")  # در رندر باید TOKEN را تعریف کنی
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_config_choice))
    app.run_polling()
