from pydantic import BaseModel


class FriendRequest(BaseModel):
    username: str


class FriendRequestResponse(BaseModel):
    '''
    Status is default so we are not adding it here
    '''

    detail: str
