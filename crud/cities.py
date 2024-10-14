from typing import List

from models.user import UserModel
from schemas.users import User


async def users_by_city(
    city: str, page: int = 1, limit: int = 10
) -> List[User]:
    '''
    Get details of users in the selected city with pagination.

    Parameters:
    - city: The city to filter users by.
    - page: The page number (default is 1).
    - limit: The number of users per page (default is 10).
    '''

    # Calculate the number of documents to skip based on the page number
    skip = (page - 1) * limit

    # Fetch users with the specified city, applying pagination
    users = (
        await UserModel.find(UserModel.selectedCity == city)
        .skip(skip)
        .limit(limit)
        .to_list()
    )

    return users
