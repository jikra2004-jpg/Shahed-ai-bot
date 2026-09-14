import os
import threading
import requests
import telebot
from flask import Flask

# ১. আপনার টেলিগ্রাম বট টোকেন দিন
TELEGRAM_BOT_TOKEN = "8983750906:AAFu3_jfQxgMrJr_LGiQLTaOMQYu_3CYzdo"

# ২. আপনার Google AI Studio থেকে আনা একদম ফ্রেশ জেমিনি এপিআই কি এখানে দিন
GEMINI_API_KEY = "AQ.Ab8RN6KzE7YoNXV1dbtM1rrBL9rzTFhiWVPIc2gHdt-9owQzmg"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram AI Bot is running smoothly!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        
        # সরাসরি গুগলের রেস্ট এপিআই (REST API) ব্যবহার করা হলো, যা কোনো ভুল বা OAuth টোকেন জেনারেট করবে না
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        # এআই-এর উত্তর বের করে আনা
        ai_reply = res_json['candidates'][0]['content']['parts'][0]['text']
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        bot.reply_to(message, f"উত্তর আনতে সমস্যা হচ্ছে: {str(e)}")

def run_telegram_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    # ব্যাকগ্রাউন্ডে টেলিগ্রাম বট চালু রাখা
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()

    # রেন্ডারের পোর্ট রিকোয়ারমেন্ট পূরণের জন্য ফ্লাস্ক সার্ভার
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
        
