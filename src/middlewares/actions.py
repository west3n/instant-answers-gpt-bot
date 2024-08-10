from aiogram import BaseMiddleware, Dispatcher
from aiogram.dispatcher.flags import get_flag
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender

from src.utils import enums

from typing import Any, Awaitable, Callable, Dict


# Middleware for sending chat actions during long operations
# You can use it in you handler registration functions as flags={'long_operation': 'typing'} or any other action
# Here is a list of available actions: https://core.telegram.org/bots/api#sendchataction
class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        long_operation_type = get_flag(data, "long_operation")

        if not long_operation_type:
            return await handler(event, data)

        async with ChatActionSender(
            bot=enums.BOT, action=long_operation_type, chat_id=event.chat.id, interval=3
        ):
            return await handler(event, data)


async def register(dp: Dispatcher):
    dp.message.middleware.register(ChatActionMiddleware())
