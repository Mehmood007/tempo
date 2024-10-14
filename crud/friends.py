from typing import List

from beanie import PydanticObjectId
from beanie.odm.operators.find.comparison import In, NotIn
from beanie.odm.operators.find.logical import Or
from fastapi import HTTPException
from starlette import status

from models.friend_request import FriendRequestModel, FriendRequestStatus
from models.user import UserModel
from schemas.friend_requests import FriendRequestResponse
from schemas.users import User


async def add_friend(
    current_user: UserModel, friend_username: str
) -> FriendRequestResponse:
    receiver_user = await UserModel.find_one(
        UserModel.userName == friend_username
    )
    '''
    Function adds friend by username to current user
    '''

    if receiver_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    receiver_id = receiver_user.id
    current_user_id = current_user.id

    # Check if they are already friends or if a request exists
    existing_request = await FriendRequestModel.find_one(
        FriendRequestModel.senderId == current_user_id,
        FriendRequestModel.receiverId == receiver_id,
    ) or await FriendRequestModel.find_one(
        FriendRequestModel.receiverId == current_user_id,
        FriendRequestModel.senderId == receiver_id,
    )

    if existing_request is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Already friends or a request has already been sent',
        )

    # Create and insert new friend request
    new_friend_request = FriendRequestModel(
        senderId=current_user_id, receiverId=receiver_id
    )
    await new_friend_request.insert()

    return {'detail': 'Friend request sent'}


async def get_friend_ids(user_id: PydanticObjectId) -> List[PydanticObjectId]:
    '''
    Function gets friend ids for specific users
    '''
    friend_requests = await FriendRequestModel.find(
        Or(
            FriendRequestModel.senderId == user_id,
            FriendRequestModel.receiverId == user_id,
        ),
        FriendRequestModel.status == FriendRequestStatus.ACCEPTED,
    ).to_list()

    return [
        (
            request.receiverId
            if request.senderId == user_id
            else request.senderId
        )
        for request in friend_requests
    ]


async def get_friends_list(user: UserModel) -> List[User]:
    '''
    Get the list of friends for the logged-in user.
    '''
    friend_ids = await get_friend_ids(user.id)

    friends = await UserModel.find(In(UserModel.id, friend_ids)).to_list()

    return friends


async def get_non_friends_list(user: UserModel) -> List[User]:
    '''
    Get the list of non friends for the logged-in user.
    '''

    friend_ids = await get_friend_ids(user.id)
    friend_ids.append(user.id)

    non_friends = await UserModel.find(
        NotIn(UserModel.id, friend_ids)
    ).to_list()

    return non_friends
