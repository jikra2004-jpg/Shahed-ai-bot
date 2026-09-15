import os
import threading
import requests
import telebot
from flask import Flask

# ১. আপনার টেলিগ্রাম বট টোকেন এখানে বসান
TELEGRAM_BOT_TOKEN = "8843921215:AAHYWadt2eYLsW8rXYNJ3VIxAHYlKKEuLv0"

# ২. আপনার জেমিনি এপিআই কি এখানে বসান
GEMINI_API_KEY = "AQ.Ab8RN6LXiVjkjT5jeyhnPs8GAMzNGxZXvJJTCXYiCtNgqtll6A"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram AI Bot is running smoothly!"

# এখানে ভুলটি ছিল, app এর পরিবর্তে সঠিকভাবে bot.message_handler ব্যবহার করা হয়েছে
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        if "candidates" in res_json:
            ai_reply = res_json["candidates"][0]["content"]["parts"][0]["text"]
            bot.reply_to(message, ai_reply)
        else:
            error_msg = res_json.get('error', {}).get('message', 'Unknown error')
            bot.reply_to(message, f"এআই রেসপন্স সমস্যা: {error_msg}")
            
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি: {str(e)}")

def run_telegram_bot():
    try:
        bot.remove_webhook()
    except:
        pass
    bot.infinity_polling(timeout=20, long_polling_timeout=10)

if __name__ == "__main__":
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
        
