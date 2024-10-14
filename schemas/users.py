from pydantic import BaseModel


class BaseUser(BaseModel):
    firstName: str
    lastName: str
    userName: str
    profilePic: str
    selectedCity: str


class CreateUser(BaseUser):
    password: str


class LoginUser(BaseModel):
    username: str
    password: str


class User(BaseUser):
    pass
