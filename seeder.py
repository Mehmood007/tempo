from passlib.context import CryptContext

from database import init_database
from main import app
from models.friend_request import FriendRequestModel
from models.user import UserModel


async def create_user(username: str) -> UserModel:
    '''
    Creates user in database and returns its model
    '''
    bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = bcrypt_context.hash('securepassword')
    user = UserModel(
        firstName='John',
        lastName='Doe',
        userName=username,
        profilePic='Just a random url',
        hashed_password=hashed_password,
        selectedCity='New York',
    )
    await user.insert()
    return user


async def seed_database():
    '''
    This function seeds database
    Its is compulsory when testing performance
    '''
    # Initialize the database connection
    await init_database(app)

    # Create sample users
    user1 = await create_user('testuser1')
    user2 = await create_user('testuser2')

    # Add other initial data as needed
    friend_request = FriendRequestModel(senderId=user1.id, receiverId=user2.id)
    await friend_request.create()

    print('Database seeded successfully!')


if __name__ == '__main__':
    import asyncio

    asyncio.run(seed_database())
