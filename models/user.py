from datetime import datetime
from typing import Optional

import pymongo
from beanie import Document, Indexed
from pydantic import Field

from .object_id import PyObjectId


class UserModel(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    firstName: str = Indexed(max_length=25)
    lastName: str = Indexed(max_length=25)
    userName: str = Indexed(max_length=50)
    hashed_password: str = Field(max_length=255)
    profilePic: str = Field(max_length=512)
    jwt_token: Optional[str] = Field(None, max_length=255)
    selectedCity: str = Indexed(max_length=50)
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        collection = 'users'
        indexes = [
            [
                ("userName", pymongo.ASCENDING),
                ("firstName", pymongo.ASCENDING),
                ("lastName", pymongo.ASCENDING),
            ],
        ]

    @property
    def full_name(self) -> str:
        return f'{self.firstName} {self.lastName}'
