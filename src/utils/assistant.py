from aiogram import types

from chatgpt_md_converter import telegram_format

from openai import AsyncOpenAI, AsyncAssistantEventHandler
from openai.types.beta.threads import TextDelta, Text

from src.utils import enums

client: AsyncOpenAI = enums.OPENAI_ASYNC_CLIENT
model = enums.OPENAI_MODEL
instruction = enums.OPENAI_ASSISTANT_INSTRUCTION


# Define Assistant class for managing assistants
class Assistant:
    @staticmethod
    async def create_new_assistant(tg_id: int) -> str:
        assistant = await client.beta.assistants.create(
            name=f"{tg_id}-assistant", model=model, instructions=instruction
        )
        return assistant.id

    @staticmethod
    async def create_new_thread() -> str:
        thread = await client.beta.threads.create()
        return thread.id

    @staticmethod
    async def create_message(thread_id: str, content: str):
        new_message = await client.beta.threads.messages.create(
            thread_id=thread_id, role="user", content=content
        )
        return new_message.id


# Define AssistantStream class for streaming assistant responses to the user
class AssistantStream(AsyncAssistantEventHandler):
    def __init__(self, message: types.Message):
        self.counter = 0
        self.message_id = 0
        self.message: types.Message = message
        super().__init__()

    async def on_text_delta(self, delta: TextDelta, snapshot: Text) -> None:
        """
        We receive text deltas from the OpenAI API, and every 10th delta we send them to the user in real-time
        :param delta: text delta, we do not use it
        :param snapshot: current stream snapshot
        :return:
        """
        self.counter += 1
        if self.counter == 1:
            message = await self.message.answer(snapshot.value)
            self.message_id = message.message_id
        else:
            if self.counter % 10 == 0:
                await self.message.bot.edit_message_text(
                    chat_id=self.message.chat.id,
                    message_id=self.message_id,
                    text=snapshot.value,
                )

    async def on_text_done(self, text: Text) -> None:
        """
        We receive the completed text from the OpenAI API and send it as markdown-formatted to the user
        :param text: completed text
        :return:
        """
        await self.message.bot.edit_message_text(
            chat_id=self.message.chat.id,
            message_id=self.message_id,
            text=telegram_format(text.value),
            parse_mode="HTML",
        )

    @staticmethod
    async def get_response_stream(
        thread_id: str, assistant_id: str, content: str, message: types.Message
    ):
        """
        Get assistant response stream
        :param thread_id: user thread id
        :param assistant_id: user assistant id
        :param content: user message
        :param message: aiogram message object for implementing real-time updates
        :return:
        """
        await Assistant.create_message(thread_id, content)
        async with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            event_handler=AssistantStream(message),
        ) as stream:
            await stream.until_done()
