from beanie import init_beanie
from decouple import config
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from models.friend_request import FriendRequestModel
from models.user import UserModel

MONGODB_DATABASE_URL = config('MONGODB_DATABASE_URL')

client = AsyncIOMotorClient(MONGODB_DATABASE_URL)
database = client.get_default_database()


async def init_database(app: FastAPI):  # pragma: no cover
    await init_beanie(
        database,
        document_models=[UserModel, FriendRequestModel],
    )
