from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from crud.cities import users_by_city
from models.user import UserModel
from schemas.users import User
from utils.authentications import current_user

router = APIRouter(
    tags=['cities'],
)


@router.get(
    '/city/users', response_model=List[User], status_code=status.HTTP_200_OK
)
async def get_users(
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=100, gt=0),
    user: UserModel = Depends(current_user),
):
    '''
    Get details of users in the selected city.
    '''
    city = user.selectedCity

    users = await users_by_city(city, page, limit)
    return users
