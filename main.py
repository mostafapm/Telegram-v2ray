import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# خواندن توکن از محیط
TOKEN = os.environ.get("TOKEN")  # در render باید TOKEN را در Environment Variables قرار بدهی

# لیست کانفیگ‌ها (در حالت واقعی میتونی از فایل یا دیتابیس بخونی)
configs = {
    "🇺🇸 کانفیگ آمریکا": "vless://uuid@us.example.com:443?security=tls&type=ws#USA",
    "🇩🇪 کانفیگ آلمان": "vless://uuid@de.example.com:443?security=tls&type=ws#Germany",
    "🇸🇬 کانفیگ سنگاپور": "vless://uuid@sg.example.com:443?security=tls&type=ws#Singapore"
}

# فرمان /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=name)] for name in configs
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("سلام 👋\nیکی از کانفیگ‌ها رو انتخاب کن:", reply_markup=reply_markup)

# وقتی کاربر یکی از کانفیگ‌ها رو انتخاب می‌کنه
async def handle_config_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_name = query.data
    config_link = configs.get(selected_name, "کانفیگ پیدا نشد.")
    await query.message.reply_text(f"🔐 کانفیگ انتخابی:\n\n`{config_link}`", parse_mode="Markdown")

# اجرای اصلی
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_config_choice))

    print("✅ ربات فعال شد.")
    app.run_polling()
