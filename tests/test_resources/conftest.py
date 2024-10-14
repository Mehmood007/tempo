import pytest
from passlib.context import CryptContext

from models.user import UserModel


@pytest.fixture
async def authenticate_client(client):
    bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
    hashed_password = bcrypt_context.hash('securepassword')
    user = UserModel(
        firstName='John',
        lastName='Doe',
        userName='johndoe',
        profilePic='Just a random url',
        hashed_password=hashed_password,
        selectedCity='New York',
    )
    await user.insert()
    response = await client.post(
        '/token', data={'username': 'johndoe', 'password': 'securepassword'}
    )
    token = response.json()['access_token']

    client.headers['Authorization'] = f'Bearer {token}'

    return client
