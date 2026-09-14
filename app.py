import os
import threading
import requests
import telebot
from flask import Flask

TELEGRAM_BOT_TOKEN = "8983750906:AAFu3_jfQxgMrJr_LGiQLTaOMQYu_3CYzdo"
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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "parts": [{"text": user_text}]
            }]
        }
        
        response = requests.post(url, json=payload, headers=headers)
        res_json = response.json()
        
        # সেফটি চেক: রেসপন্সে candidates আছে কি না তা যাচাই করা
        if "candidates" in res_json and len(res_json["candidates"]) > 0:
            candidate = res_json["candidates"][0]
            if "content" in candidate and "parts" in candidate["content"]:
                ai_reply = candidate["content"]["parts"][0]["text"]
                bot.reply_to(message, ai_reply)
            else:
                bot.reply_to(message, f"এআই থেকে ফরম্যাট ঠিকমতো আসেনি: {res_json}")
        else:
            # যদি গুগল এপিআই থেকে কোনো এরর দেয় (যেমন কোটা শেষ বা ইনভ্যালিড কি)
            bot.reply_to(message, f"এপিআই রেসপন্স এরর: {res_json}")
            
    except Exception as e:
        bot.reply_to(message, f"কোডে সমস্যা হয়েছে: {str(e)}")

def run_telegram_bot():
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
        
