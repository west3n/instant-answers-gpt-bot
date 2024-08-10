from aiogram import types, Dispatcher, F

from src.database.models import User
from src.utils.assistant import AssistantStream


# Handle conversation message
async def handle_message(message: types.Message):
    user = await User.find_one(User.tg_id == message.from_user.id)
    await AssistantStream.get_response_stream(
        thread_id=user.thread_id,
        assistant_id=user.assistant_id,
        content=message.text,
        message=message,
    )


async def register(dp: Dispatcher):
    dp.message.register(handle_message, F.text, flags={"long_operation": "typing"})
