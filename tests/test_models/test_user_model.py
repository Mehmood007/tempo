from datetime import datetime

import pytest
from bson import ObjectId

from models.object_id import PyObjectId
from models.user import UserModel


@pytest.mark.asyncio
async def test_user_model_creation():
    user = UserModel(
        firstName='John',
        lastName='Doe',
        userName='johndoe',
        hashed_password='hashed Password',
        profilePic='http://example.com/profile.jpg',
        jwt_token='some_jwt_token',
        selectedCity='New York',
    )
    assert user.firstName == 'John'
    assert user.lastName == 'Doe'
    assert user.userName == 'johndoe'
    assert user.profilePic == 'http://example.com/profile.jpg'
    assert user.jwt_token == 'some_jwt_token'
    assert user.selectedCity == 'New York'
    assert isinstance(user.created_at, datetime)


@pytest.mark.asyncio
async def test_user_model_full_name():
    user = UserModel(
        firstName='Jane',
        lastName='Doe',
        userName='janedoe',
        hashed_password='hashed Password',
        profilePic='http://example.com/profile.jpg',
        jwt_token=None,
        selectedCity='Los Angeles',
    )
    assert user.full_name == 'Jane Doe'


@pytest.mark.asyncio
async def test_user_model_invalid_username():
    with pytest.raises(ValueError):
        UserModel(
            firstName='John',
            lastName='Doe',
            userName=('a' * 51),
            profilePic='http://example.com/profile.jpg',
            jwt_token='some_jwt_token',
            selectedCity='New York',
        )


def test_valid_object_id():
    valid_id = ObjectId()
    obj_id = PyObjectId.validate(valid_id)
    assert isinstance(obj_id, ObjectId)
    assert obj_id == valid_id


def test_valid_object_id_string():
    valid_id_str = str(ObjectId())
    obj_id = PyObjectId.validate(valid_id_str)
    assert isinstance(obj_id, ObjectId)
    assert obj_id == ObjectId(valid_id_str)


def test_invalid_object_id():
    with pytest.raises(ValueError) as excinfo:
        PyObjectId.validate('invalid_object_id')
    assert str(excinfo.value) == 'Invalid ObjectId'


def test_invalid_object_id_short_string():
    with pytest.raises(ValueError) as excinfo:
        PyObjectId.validate('123')
    assert str(excinfo.value) == 'Invalid ObjectId'


def test_invalid_object_id_long_string():
    with pytest.raises(ValueError) as excinfo:
        PyObjectId.validate('a' * 25)
    assert str(excinfo.value) == 'Invalid ObjectId'


def test_invalid_object_id_none():
    with pytest.raises(ValueError) as excinfo:
        PyObjectId.validate(None)
    assert str(excinfo.value) == 'Invalid ObjectId'


def test_invalid_object_id_empty_string():
    with pytest.raises(ValueError) as excinfo:
        PyObjectId.validate('')
    assert str(excinfo.value) == 'Invalid ObjectId'
