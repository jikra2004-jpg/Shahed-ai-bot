import os
import telebot
import google.generativeai as genai

# টেলিগ্রাম এবং জেমিনি এপিআই টোকেন
TELEGRAM_BOT_TOKEN = "8983750906:AAEE_sk6GIwhSKC3-Nczyiz90GTnDyNqmno"
GEMINI_API_KEY = "AQ.Ab8RN6LrGQKZ3rKZ1HQgdtT6ihV8SXr2WpkKm1cfBbCLLQY7Ug"

# কনফিগারেশন
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_message = message.text
    try:
        # জেমিনি এআই থেকে উত্তর নিয়ে আসা
        response = model.generate_content(user_message)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "দুঃখিত, এই মুহূর্তে উত্তর দিতে সমস্যা হচ্ছে।")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()

