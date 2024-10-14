from datetime import datetime, timedelta, timezone
from typing import Annotated, Union

from beanie import PydanticObjectId
from decouple import config
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from starlette import status

from constants import HASH_ALGORITHM
from models.user import UserModel
from schemas.token import JWT_Token

SECRET_KEY = config('SECRET_KEY')

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


async def authenticate(username: str, password: str) -> Union[bool, UserModel]:
    user = await UserModel.find_one(UserModel.userName == username)

    if not user or not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


async def current_user(
    token: Annotated[str, Depends(oauth2_bearer)]
) -> UserModel:
    '''
    Fetch User for JSON Web Token (JWT)

    This method is used during authorization
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, HASH_ALGORITHM)
        username: str = payload.get('sub')
        user_id: PydanticObjectId = payload.get('id')
        if not (username and user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token',
            )
        user = await UserModel.get(user_id)
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token'
        )


def create_jwt(
    username: str, user_id: PydanticObjectId, expire_delta: timedelta
) -> str:
    '''
    Create a JSON Web Token (JWT) for user authentication.

    This is called once user is authenticated
    '''
    encode = {'sub': username, 'id': str(user_id)}
    expires = datetime.now(timezone.utc) + expire_delta
    encode.update({'exp': expires})

    return jwt.encode(encode, SECRET_KEY, HASH_ALGORITHM)


async def login_user(username: str, password: str) -> JWT_Token:
    '''
    Authenticate user and return JWT to authenticated user
    '''
    user = await authenticate(username, password)
    if user:
        token = create_jwt(user.userName, user.id, timedelta(minutes=60))
        user.jwt_token = token
        await user.save()
        return {'access_token': token, 'token_type': 'bearer'}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credentials',
    )
