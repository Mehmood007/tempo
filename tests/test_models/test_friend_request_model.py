import pytest

from models.friend_request import FriendRequestModel

from ..factories.user_factory import UserModelFactory


@pytest.mark.asyncio
async def test_friend_request_model_creation(user):
    friend = UserModelFactory()

    friend_request = FriendRequestModel(
        senderId=user.id,
        receiverId=friend.id,
        status='accepted',
    )

    assert friend_request.status == 'accepted'


@pytest.mark.asyncio
async def test_friend_request_properties(user):
    friend = UserModelFactory()
    friend = await friend.insert()

    friend_request = FriendRequestModel(
        senderId=user.id,
        receiverId=friend.id,
        status='accepted',
    )

    # Await the asynchronous properties
    sender = await friend_request.sender
    receiver = await friend_request.receiver

    assert sender.id == user.id
    assert receiver.id == friend.id
