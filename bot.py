from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import asyncio
import os

BOT_TOKEN = "8943413347:AAH4c5g_arJB3CM-3n1elkiCwU7v0wLmvWM"
GEMINI_API_KEY = "AIzaSyBKMwsVbs2vGeBUAEXcRau8UTSyX_4a7oI"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

telegram_app = Application.builder().token(BOT_TOKEN).build()

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = model.generate_content(user_message)

    await update.message.reply_text(response.text)

telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)

    asyncio.run(telegram_app.process_update(update))

    return "ok"

@app.route("/")
def home():
    return "Bot is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)