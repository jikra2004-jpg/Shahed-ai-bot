import os
import threading
import requests
import telebot
from flask import Flask

# আপনার টেলিগ্রাম বট টোকেন এখানে দিন
TELEGRAM_BOT_TOKEN = "8983750906:AAFu3_jfQxgMrJr_LGiQLTaOMQYu_3CYzdo"

# Google AI Studio থেকে আনা একদম নতুন সঠিক এপিআই কি এখানে দিন
GEMINI_API_KEY = "AQ.Ab8RN6KwSs1nvvD_r6okS40teLGP_0a2QxNiJBhWQ3rcqlWP_A"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram AI Bot is running!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        user_text = message.text
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
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
            bot.reply_to(message, f"এপিআই রেসপন্স সমস্যা: {res_json.get('error', {}).get('message', 'Unknown error')}")
            
    except Exception as e:
        bot.reply_to(message, f"ত্রুটি: {str(e)}")

def run_telegram_bot():
    # কনফ্লিক্ট এড়ানোর জন্য আগের সমস্ত ওয়েবহুক রিমूव করে ফ্রেশ পোলিং শুরু করা
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
        
