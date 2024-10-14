from datetime import datetime
from enum import Enum
from typing import Optional

from beanie import Document
from pydantic import Field

from models.user import UserModel

from .object_id import PyObjectId


class FriendRequestStatus(str, Enum):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    BLOCKED = 'blocked'


class FriendRequestModel(Document):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    senderId: PyObjectId = Field(
        description='ID of the user sending the friend request',
    )
    receiverId: PyObjectId = Field(
        description='ID of the user receiving the friend request',
    )
    status: FriendRequestStatus = Field(default=FriendRequestStatus.ACCEPTED)
    created_at: datetime = Field(default_factory=datetime.now)

    class Settings:
        name = 'friendrequests'

    @property
    async def sender(self) -> Optional[UserModel]:
        return await UserModel.get(self.senderId)

    @property
    async def receiver(self) -> Optional[UserModel]:
        return await UserModel.get(self.receiverId)
