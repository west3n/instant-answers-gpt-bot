import math

from aiogram import Bot


class ChunkLimitError(Exception):
    """Custom exception raised when the number of chunks exceeds the limit."""

    pass


class Stream:
    # Class for stream answers of plain texts
    def __init__(self, bot: Bot, text: str, chunks_amount: int):
        if chunks_amount > 10:
            raise ChunkLimitError("The number of chunks exceeds the limit of 10.")

        self.bot = bot
        self.text = text
        self.chunks_amount = chunks_amount

    def split_text(self):
        # Method for splitting text into chunks
        chunk_size = math.ceil(len(self.text) / self.chunks_amount)
        text_chunks = [
            self.text[i: i + chunk_size] for i in range(0, len(self.text), chunk_size)
        ]
        return text_chunks

    async def answer(self, chat_id: int):
        text_chunks = self.split_text()
        # Send the first chunk as a message
        message = await self.bot.send_message(chat_id, text_chunks[0])
        message_id = message.message_id  # Capture the message ID for editing

        # Send the subsequent chunks by summarizing and editing the previous message
        for i in range(1, len(text_chunks)):
            new_text = "".join(text_chunks[: i + 1])
            await self.bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=new_text
            )
