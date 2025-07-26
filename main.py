import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# لیست کانفیگ‌ها (تو اینجا می‌تونی کانفیگ‌های واقعی‌تو بذاری)
configs = {
    "کانفیگ Reality ایران": "vless://uuid1@host1:443?security=reality&encryption=none...",
    "کانفیگ V2ray با TLS": "vless://uuid2@host2:443?path=/&security=tls&type=ws...",
    "کانفیگ GRPC Cloudflare": "vless://uuid3@host3:443?mode=gun&security=reality&type=grpc..."
}

# دستور /start - نمایش لیست کانفیگ‌ها
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(name, callback_data=name)] for name in configs.keys()]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 خوش آمدید!\nلطفاً یکی از کانفیگ‌ها را برای خرید انتخاب کنید:", reply_markup=reply_markup)

# انتخاب کانفیگ توسط کاربر
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    selected_config = query.data
    context.user_data["selected_config"] = selected_config
    await query.message.reply_text(
        f"💳 برای خرید «{selected_config}»، لطفاً مبلغ را کارت به کارت کرده و رسید را ارسال کنید:\n\n"
        "شماره کارت: 6037-9911-1234-5678\n"
        "به نام: علی محمدی\n\n"
        "✅ بعد از ارسال رسید، کانفیگ برای شما ارسال می‌شود."
    )

# دریافت رسید تصویری و ارسال کانفیگ
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    selected = context.user_data.get("selected_config")
    if selected:
        config = configs.get(selected, "❌ کانفیگ یافت نشد.")
        await update.message.reply_text(f"✅ رسید دریافت شد.\n📡 کانفیگ شما:\n\n{config}")
    else:
        await update.message.reply_text("❌ لطفاً اول یک کانفیگ انتخاب کنید با دستور /start")

# دریافت پیام‌های دیگر (هشدار)
async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📷 لطفاً رسید پرداخت را به صورت عکس ارسال کنید.")

# اجرای ربات
if __name__ == "__main__":
    TOKEN = os.environ.get("TOKEN")  # توکن را از محیط اجرا می‌گیره (Render)
    if not TOKEN:
        print("❌ توکن پیدا نشد. متغیر TOKEN را در محیط تنظیم کنید.")
        exit()

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_other))

    print("✅ ربات در حال اجراست...")
    app.run_polling()
