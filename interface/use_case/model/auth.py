from pydantic import BaseModel

from interface.use_case.model.base_response import BaseResponse


class TokenData(BaseModel):
    email: str
    user_id: str
    username: str
    roles: list[str]

class TokenResponse(BaseResponse):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int