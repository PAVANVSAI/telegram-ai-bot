from flask import Flask, request
from telegram import Bot, Update
from openai import OpenAI
import asyncio

# =========================
# YOUR TOKENS
# =========================
import os

BOT_TOKEN = "8943413347:AAH4c5g_arJB3CM-3n1elkiCwU7v0wLmvWM"

OPENROUTER_API_KEY = "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"


# =========================
# OPENROUTER CLIENT
# =========================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# =========================
# TELEGRAM BOT
# =========================

bot = Bot(token=BOT_TOKEN)

app = Flask(__name__)

# =========================
# WEBHOOK
# =========================

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        update = Update.de_json(data, bot)

        if update.message and update.message.text:

            user_message = update.message.text

            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://telegram-ai-bot-3yur.onrender.com",
                    "X-Title": "telegram-ai-bot",
                },
                model="meta-llama/llama-3-8b-instruct:free",
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

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return "Bot is running!"

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)