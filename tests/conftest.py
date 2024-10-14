import pytest
from beanie import init_beanie
from decouple import config
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from main import app
from models.friend_request import FriendRequestModel
from models.user import UserModel

from .factories.user_factory import UserModelFactory


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as client_instance:
        yield client_instance


@pytest.fixture(scope='function', autouse=True)
async def init_db():
    client = AsyncIOMotorClient(config('MONGODB_TEST_DATABASE_URL'))
    database = client.get_default_database()
    await init_beanie(
        database,
        document_models=[
            UserModel,
            FriendRequestModel,
        ],
    )

    yield database

    await client.drop_database(database.name)
    client.close()


@pytest.fixture
async def user():
    user = UserModelFactory()
    await user.insert()

    return user
