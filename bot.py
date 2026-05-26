from flask import Flask, request
from telegram import Bot, Update
from openai import OpenAI
import asyncio
import os

BOT_TOKEN = "8943413347:AAH4c5g_arJB3CM-3n1elkiCwU7v0wLmvWM"

GROQ_API_KEY = "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"

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        update = Update.de_json(data, bot)

        if update.message and update.message.text:

            user_message = update.message.text

            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            reply_text = completion.choices[0].message.content

            asyncio.run(
                bot.send_message(
                    chat_id=update.message.chat.id,
                    text=reply_text
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