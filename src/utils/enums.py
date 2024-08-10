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
MONGO_STRING = "mongodb://mongo:27017/admin"
