# main.py
import os
import json
import asyncio
from datetime import datetime

import aiofiles
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

# Загружаем .env
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Положи BOT_TOKEN в файл .env")

app = FastAPI()

DATA_FILE = "data.json"


# Инициализация пустого json-файла
async def init_json():
    if not os.path.exists(DATA_FILE):
        async with aiofiles.open(DATA_FILE, "w", encoding="utf-8") as f:
            await f.write("[]")


# Сохранение сообщения в json
async def save_message(data: dict):
    async with aiofiles.open(DATA_FILE, "r+", encoding="utf-8") as f:
        content = await f.read()
        json_data = json.loads(content) if content.strip() else []
        json_data.append(data)
        await f.seek(0)
        await f.truncate()
        await f.write(json.dumps(json_data, ensure_ascii=False, indent=2))


# Обработчик всех сообщений от пользователя
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    user = msg.from_user

    entry = {
        "timestamp": datetime.now().isoformat(),
        "chat_id": msg.chat_id,
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "text": msg.text or msg.caption or "[не текст]",
    }

    await save_message(entry)
    await msg.reply_text("Сохранено локально")


# Запуск Telegram-бота в фоне
async def run_bot():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, message_handler))

    await application.initialize()
    await application.start()
    print("Бот запущен и активно опрашивает Telegram...")

    # Эта строчка — ключ к жизни в Termux
    await application.updater.start_polling(
        poll_interval=2.0,
        timeout=20,
        bootstrap_retries=-1,
        allowed_updates=Update.ALL_TYPES
    )
    
    await asyncio.Event().wait()  # держим задачу живой


# ==================== FastAPI ====================

@app.on_event("startup")
async def on_startup():
    await init_json()
    asyncio.create_task(run_bot())  # запускаем бота в фоне


@app.get("/")
async def root():
    return {"status": "ok", "msg": "Telegram → JSON работает"}


@app.get("/data")
async def get_all_data():
    try:
        async with aiofiles.open(DATA_FILE, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content) if content.strip() else []
        return data
    except Exception as e:
        return {"error": str(e)}
