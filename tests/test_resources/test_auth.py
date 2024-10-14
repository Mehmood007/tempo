import pytest
from starlette import status


@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post(
        '/auth',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'userName': 'johndoe',
            'password': 'securepassword',
            'profilePic': 'http://example.com/profile.jpg',
            'selectedCity': 'New York',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['userName'] == 'johndoe'


@pytest.mark.asyncio
async def test_create_existing_username(client):
    await test_create_user(client)

    response = await client.post(
        '/auth',
        json={
            'firstName': 'John',
            'lastName': 'Doe',
            'userName': 'johndoe',
            'password': 'securepassword',
            'profilePic': 'http://example.com/profile.jpg',
            'selectedCity': 'New York',
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['detail'] == 'Username already exists'


@pytest.mark.asyncio
async def test_login(client):
    await test_create_user(client)

    response = await client.post(
        '/login',
        json={'username': 'johndoe', 'password': 'securepassword'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()


@pytest.mark.asyncio
async def test_invalid_login(client):
    await test_create_user(client)

    response = await client.post(
        '/login',
        json={'username': 'johndoe', 'password': 'wrongpassword'},
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert 'access_token' not in response.json()


@pytest.mark.asyncio
async def test_login_success(client):
    await test_create_user(client)
    response = await client.post(
        '/token', data={'username': 'johndoe', 'password': 'securepassword'}
    )
    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_login_failure(client, user):
    response = await client.post(
        '/token', data={'username': 'wronguser', 'password': 'wrongpassword'}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid credentials'}
