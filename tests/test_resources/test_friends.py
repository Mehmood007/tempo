import pytest
from starlette import status

from models.friend_request import FriendRequestModel
from models.user import UserModel


@pytest.mark.asyncio
async def test_invalid_username_friend_request(authenticate_client):
    response = await authenticate_client.post(
        '/friend/request', json={'username': 'non existing user'}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_existing_friend_request(authenticate_client, user):
    authenticated_user = await UserModel.find_one(
        UserModel.userName == 'johndoe'
    )
    new_friend_request = FriendRequestModel(
        senderId=user.id, receiverId=authenticated_user.id
    )
    await new_friend_request.insert()

    response = await authenticate_client.post(
        '/friend/request', json={'username': user.userName}
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_create_friend_request(authenticate_client, user):
    response = await authenticate_client.post(
        '/friend/request', json={'username': user.userName}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['detail'] == 'Friend request sent'


@pytest.mark.asyncio
async def test_friends_list(authenticate_client, user):
    await test_create_friend_request(authenticate_client, user)
    response = await authenticate_client.get(
        '/friends', headers={'Cache-Control': 'no-store'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_non_friends_list(authenticate_client, user):
    response = await authenticate_client.get(
        '/not-friends', headers={'Cache-Control': 'no-store'}
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
