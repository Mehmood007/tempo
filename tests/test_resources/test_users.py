import pytest
from decouple import config
from jose import jwt
from starlette import status

from .test_auth import test_create_user


@pytest.mark.asyncio
async def test_get_user(authenticate_client, user):
    user_id = user.id
    response = await authenticate_client.get(f'/users/{user_id}')

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_non_existing_user(authenticate_client):
    fake_user_id = '5eb7cf5a86d9755df3a6c593'
    response = await authenticate_client.get(f'/users/{fake_user_id}')

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_unauthenticated_user(client):
    fake_user_id = '5eb7cf5a86d9755df3a6c593'
    response = await client.get(f'/users/{fake_user_id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_invalid_token(client):
    await test_create_user(client)
    response = await client.post(
        '/token', data={'username': 'johndoe', 'password': 'securepassword'}
    )
    token = response.json()['access_token']

    client.headers['Authorization'] = f'Bearer {token} invalid'

    fake_user_id = '5eb7cf5a86d9755df3a6c593'
    response = await client.get(f'/users/{fake_user_id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_missing_fields_in_token(client):
    token_with_missing_fields = jwt.encode(
        {'other_field': 'value'}, config('SECRET_KEY'), algorithm='HS256'
    )

    fake_user_id = '5eb7cf5a86d9755df3a6c593'
    response = await client.get(
        f'/users/{fake_user_id}',
        headers={'Authorization': f'Bearer {token_with_missing_fields}'},
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid token'}
