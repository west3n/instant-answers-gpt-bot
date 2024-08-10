from aiogram.types import BotCommand

from src.handlers.commands import register as register_commands
from src.handlers.conversation import register as register_conversation

from src.middlewares.actions import register as register_actions_middlewares
from src.utils import enums


# Register commands
async def commands_registration():
    await enums.BOT.set_my_commands(
        [
            BotCommand(command="start", description="Run Bot"),
            BotCommand(command="clear_history", description="Clear history"),
        ]
    )


# Register handlers
async def handlers_registration(dp):
    await register_commands(dp)
    await register_conversation(dp)


# Register middlewares
async def middlewares_registration(dp):
    await register_actions_middlewares(dp)
