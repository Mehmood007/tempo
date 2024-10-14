from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from models.user import UserModel
from schemas.users import User
from utils.authentications import current_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def get_user(
    user_id: PydanticObjectId, user: UserModel = Depends(current_user)
):
    '''
    Get details of a specific user.
    '''
    user = await UserModel.get(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return user
