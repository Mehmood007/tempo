import pytest
from starlette import status

from models.user import UserModel


@pytest.mark.asyncio
async def test_get_city_users(authenticate_client):
    response = await authenticate_client.get('/city/users')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_city_multiple_users(authenticate_client, user):
    authenticated_user = await UserModel.find_one(
        UserModel.userName == 'johndoe'
    )
    user.selectedCity = authenticated_user.selectedCity
    await user.save()
    response = await authenticate_client.get('/city/users')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2
