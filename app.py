import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler

# توکن از متغیر محیطی خوانده می‌شود (امن‌تر)
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# آدرس سرور Render خودت را اینجا می‌گذاری (بعداً پر می‌کنیم)
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")

app = Flask(__name__)
telegram_app = Application.builder().token(TOKEN).build()

# ========== تابع /start ==========
async def start(update: Update, context):
    await update.message.reply_text(
        "Hello to you 👋🏻☘️\n"
        "Please send your details and photo so it can be uploaded to the channel 🌍🌌"
    )

telegram_app.add_handler(CommandHandler("start", start))

# ========== مسیرهای Flask ==========
@app.route("/")
def home():
    return "Bot is running!"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    telegram_app.update_queue.put(update)
    return "OK", 200

# ========== راه‌اندازی Webhook ==========
async def setup_webhook():
    await telegram_app.bot.set_webhook(f"{RENDER_URL}/webhook/{TOKEN}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(telegram_app.initialize())
    asyncio.run(setup_webhook())
    asyncio.run(telegram_app.start())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
