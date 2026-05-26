from flask import Flask, request
from telegram import Bot, Update
from openai import OpenAI
import asyncio

BOT_TOKEN = "8943413347:AAH4c5g_arJB3CM-3n1elkiCwU7v0wLmvWM"
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
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
                model="meta-llama/llama-3-8b-instruct:free",
                messages=[
                    {"role": "user", "content": user_message}
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