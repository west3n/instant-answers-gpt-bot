from aiogram import types, Dispatcher
from aiogram.filters import CommandStart, Command

from src.database.models import User
from src.utils import enums
from src.utils.stream import Stream
from src.utils.assistant import Assistant


async def start(message: types.Message):
    user = await User.find_one(User.tg_id == message.from_user.id)
    if not user:
        # Create new user in the database if it doesn't exist
        assistant_id = await Assistant.create_new_assistant(message.from_user.id)
        thread_id = await Assistant.create_new_thread()
        new_user = User(
            tg_id=message.from_user.id, assistant_id=assistant_id, thread_id=thread_id
        )
        await new_user.insert()

    # Use Stream class to send chunks of text to the user in stream mode
    stream = Stream(enums.BOT, "Hello, how can I help you today?", 3)
    await stream.answer(message.chat.id)


async def clear_history(message: types.Message):
    # Clear history by deleting existing thread and creating a new one
    user = await User.find_one(User.tg_id == message.from_user.id)
    new_thread_id = await Assistant.create_new_thread()
    user.thread_id = new_thread_id
    await user.save()

    # Use Stream class to send chunks of text to the user in stream mode
    stream = Stream(enums.BOT, "History has been cleared.", 3)
    await stream.answer(message.chat.id)


async def register(dp: Dispatcher):
    dp.message.register(start, CommandStart())
    dp.message.register(clear_history, Command("clear_history"))
