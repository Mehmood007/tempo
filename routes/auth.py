from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from crud.users import create_user
from schemas.users import CreateUser, LoginUser
from utils.authentications import login_user

router = APIRouter(
    tags=['auth'],
)


@router.post('/auth', status_code=status.HTTP_201_CREATED)
async def sign_up(user: CreateUser):
    '''
    This method is used to signup new user
    '''

    user = await create_user(user)

    return user


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(login_request: LoginUser):
    '''
    Authenticate user and return JWT to authenticated user
    '''
    token = await login_user(login_request.username, login_request.password)
    return token


@router.post('/token', status_code=status.HTTP_200_OK)
async def swagger_login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    '''
    This login is method is primarily used in SWAGGER
    '''
    token = await login_user(form_data.username, form_data.password)
    return token
