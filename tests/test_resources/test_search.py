import pytest
from starlette import status


@pytest.mark.asyncio
async def test_search_invalid_user(authenticate_client):
    response = await authenticate_client.get('/search/users')
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_search_valid_user(authenticate_client):
    response = await authenticate_client.get(
        '/search/users?first_name=John&last_name=Doe&username=johndoe'
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1
