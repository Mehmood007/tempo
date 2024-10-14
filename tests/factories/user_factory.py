from datetime import datetime

import factory
from factory import Faker

from models.object_id import PyObjectId
from models.user import UserModel


class UserModelFactory(factory.Factory):
    class Meta:
        model = UserModel

    id = factory.LazyFunction(PyObjectId)  # Generate a new PyObjectId
    firstName = Faker('first_name')
    lastName = Faker('last_name')
    userName = Faker('user_name')
    hashed_password = Faker('password')
    profilePic = Faker('image_url')
    jwt_token = None
    selectedCity = Faker('city')
    created_at = factory.LazyFunction(datetime.now)
