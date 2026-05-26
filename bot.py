from flask import Flask, request
from telegram import Bot, Update
import google.generativeai as genai
import asyncio

BOT_TOKEN = "8943413347:AAH4c5g_arJB3CM-3n1elkiCwU7v0wLmvWM"
GEMINI_API_KEY = "AIzaSyBKMwsVbs2vGeBUAEXcRau8UTSyX_4a7oI"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        update = Update.de_json(data, bot)

        if update.message and update.message.text:

            user_message = update.message.text

            response = model.generate_content(user_message)

            asyncio.run(
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text=response.text
                )
            )

        return "ok"

    except Exception as e:
        print(e)
        return "error"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)