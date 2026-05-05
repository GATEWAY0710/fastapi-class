from pydantic import BaseModel


class TokenData(BaseModel):
    email: str
    user_id: str
    username: str
    roles: list[str]