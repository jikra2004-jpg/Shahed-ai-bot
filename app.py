import os
import threading
import telebot
import google.generativeai as genai
from flask import Flask

# এখানে সরাসরি আপনার আসল টোকেন এবং এপিআই কি বসিয়ে দিন
TELEGRAM_BOT_TOKEN = "8983750906:AAEE_sk6GIwhSKC3-Nczyiz90GTnDyNqmno"
GEMINI_API_KEY = "AQ.Ab8RN6KzE7YoNXV1dbtM1rrBL9rzTFhiWVPIc2gHdt-9owQzmg"
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram AI Bot is running!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"দুঃখিত, সমস্যা হয়েছে: {str(e)}")

def run_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে টেলিগ্রাম বট রান করা
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()

    # রেন্ডারের জন্য ফ্লাস্ক সার্ভার চালু করা
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
