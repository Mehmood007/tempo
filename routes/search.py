from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from starlette import status

from crud.users import find_users
from models.user import UserModel
from schemas.users import User
from utils.authentications import current_user

router = APIRouter(
    prefix='/search',
    tags=['search'],
)


@router.get(
    '/users', response_model=List[User], status_code=status.HTTP_200_OK
)
async def search_users(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
    page: int = Query(default=1, gt=0),
    limit: int = Query(default=100, gt=0),
    user: UserModel = Depends(current_user),
):
    '''
    This endpoint is used to search users with city
    '''
    users = await find_users(
        user.selectedCity,
        first_name,
        last_name,
        username,
        page,
        limit,
    )

    return users
