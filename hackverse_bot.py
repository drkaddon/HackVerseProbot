from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# === Replace with your bot token ===
BOT_TOKEN = "8137627040:AAHb9ZOkhAcFluguQtDE-zRSUPcgwzW7suY"

# === QR image link ===
QR_IMAGE_URL = "https://www.mediafire.com/convkey/bd29/5lvm7mstbmv9tvtzg.jpg"

hacks = {
    "Mine Hack": {"week": 499, "month": 899},
    "Aviator Hack": {"week": 499, "month": 999},
    "Chicken Road Hack": {"week": 399, "month": 799},
    "Fruit Blast Hack": {"week": 449, "month": 849},
    "Zupee Hack": {"week": 549, "month": 999},
    "777 Hack": {"week": 599, "month": 1049}
}

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(hack, callback_data=hack)] for hack in hacks
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select a hack:", reply_markup=reply_markup)

async def hack_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    hack = query.data
    user_data[query.from_user.id] = hack

    price_buttons = [
        [InlineKeyboardButton(f"1 Week - ₹{hacks[hack]['week']}", callback_data="week")],
        [InlineKeyboardButton(f"1 Month - ₹{hacks[hack]['month']}", callback_data="month")]
    ]
    reply_markup = InlineKeyboardMarkup(price_buttons)
    await query.answer()
    await query.edit_message_text(f"You selected: {hack}\nNow choose a plan:", reply_markup=reply_markup)

async def plan_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    plan = query.data
    hack = user_data.get(query.from_user.id, "")
    price = hacks[hack][plan]
    
    await query.answer()
    await query.edit_message_text(f"Pay ₹{price} via the QR below:")
    await context.bot.send_photo(chat_id=query.message.chat_id, photo=QR_IMAGE_URL)
    await context.bot.send_message(chat_id=query.message.chat_id, text="Send your transaction ID after payment.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text:
        await update.message.reply_text("✅ Thank you! Please wait a few minutes. We are verifying your payment.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(hack_selected, pattern="^(Mine Hack|Aviator Hack|Chicken Road Hack|Fruit Blast Hack|Zupee Hack|777 Hack)$"))
    app.add_handler(CallbackQueryHandler(plan_selected, pattern="^(week|month)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot is running... Press Ctrl+C to stop")
    app.run_polling()
