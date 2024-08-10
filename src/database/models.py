from beanie import init_beanie, Document
from motor.motor_asyncio import AsyncIOMotorClient

from src.utils import enums

# Define constants
mongo_string = enums.MONGO_STRING


# Define user Beanie document model
class User(Document):
    tg_id: int
    assistant_id: str
    thread_id: str

    class Settings:
        name = "users"
        keep_nulls = False


# Initialize the database
async def init_database():
    client = AsyncIOMotorClient(mongo_string)

    await init_beanie(database=client.db_name, document_models=[User])
