from pydantic import BaseModel


class JWT_Token(BaseModel):
    access_token: str
    token_type: str
