import os

from aiogram import Bot
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# Telegram
BOT = Bot(token=os.getenv("BOT_TOKEN"))

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_ASYNC_CLIENT = AsyncOpenAI(api_key=OPENAI_API_KEY)
OPENAI_MODEL = "gpt-4o-mini"
OPENAI_ASSISTANT_INSTRUCTION = "You are a helpful assistant."

# MongoDB
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
# MONGO_STRING = f'mongodb://{MONGO_USER}:{MONGO_PASSWORD}@localhost:27017/admin'
MONGO_STRING = "mongodb://mongo:27017/admin"
