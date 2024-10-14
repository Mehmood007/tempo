import re
from typing import List, Optional

from beanie.odm.operators.find.logical import And
from fastapi import HTTPException
from starlette import status

from models.user import UserModel
from schemas.users import CreateUser, User
from utils.authentications import bcrypt_context


async def create_user(user: CreateUser) -> CreateUser:
    '''
    This method is used to signup new user
    '''

    existing_user = await UserModel.find_one(
        UserModel.userName == user.userName
    )
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username already exists',
        )

    hashed_password = bcrypt_context.hash(user.password)

    user_model = UserModel(
        firstName=user.firstName,
        lastName=user.lastName,
        userName=user.userName,
        profilePic=user.profilePic,
        hashed_password=hashed_password,
        selectedCity=user.selectedCity,
    )

    await user_model.insert()

    return user


async def find_users(
    selectedCity: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    username: Optional[str] = None,
    page: int = 1,
    limit: int = 100,
) -> List[User]:
    '''
    This endpoint is used to search users with city
    '''
    if not (first_name or last_name or username):
        raise HTTPException(
            status_code=400,
            detail='At least one search parameter is required.',
        )

    # Start the query with the city condition
    query = UserModel.selectedCity == selectedCity

    # Create a list to hold the conditions
    conditions = [query]

    # Add conditions based on provided parameters
    if first_name:
        first_name = re.compile(first_name, re.IGNORECASE)
        conditions.append(UserModel.firstName == first_name)

    if last_name:
        last_name = re.compile(last_name, re.IGNORECASE)
        conditions.append(UserModel.lastName == last_name)

    if username:
        username = re.compile(username, re.IGNORECASE)
        conditions.append(UserModel.userName == username)

    # Combine conditions using And
    combined_query = And(*conditions)

    skip = (page - 1) * limit

    # Fetch matching users
    users = (
        await UserModel.find(combined_query).skip(skip).limit(limit).to_list()
    )

    return users
