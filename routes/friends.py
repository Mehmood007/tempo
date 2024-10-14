from typing import List

from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
from starlette import status

from constants import CACHE_TIME
from crud.friends import add_friend, get_friends_list, get_non_friends_list
from models.user import UserModel
from schemas.friend_requests import FriendRequest, FriendRequestResponse
from schemas.users import User
from utils.authentications import current_user

router = APIRouter(tags=['friends'])


@router.post(
    '/friend/request',
    response_model=FriendRequestResponse,
    status_code=status.HTTP_200_OK,
)
async def send_friend_request(
    friend_request: FriendRequest, user: UserModel = Depends(current_user)
):
    '''
    Send Friend Request to Another User
    '''
    receiver_username = friend_request.username
    response = await add_friend(user, receiver_username)

    return response


@router.get(
    '/friends', response_model=List[User], status_code=status.HTTP_200_OK
)
@cache(expire=CACHE_TIME)
async def get_friends(user: UserModel = Depends(current_user)):
    '''
    Get the list of friends for the logged-in user.
    '''

    friends = await get_friends_list(user)

    return friends


@router.get(
    '/not-friends', response_model=List[User], status_code=status.HTTP_200_OK
)
@cache(expire=CACHE_TIME)
async def get_non_friends(user: UserModel = Depends(current_user)):
    '''
    Get the list of non friends for the logged-in user.
    '''

    non_friends = await get_non_friends_list(user)
    return non_friends
