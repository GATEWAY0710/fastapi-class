from typing import Optional, List

from pydantic import BaseModel, EmailStr, UUID4

from interface.use_case.model.base_response import BaseResponse


class CreateUser(BaseModel):
    email: EmailStr
    username: Optional[str]
    password: str
    confirm_password: str

    def validate_password(self):
        return self.password == self.confirm_password

class UserResponse(BaseResponse):
    id: UUID4
    email: EmailStr
    username: str

class Get(BaseModel):
    id: str

class GetResponse(BaseResponse):
    id: UUID4
    email: EmailStr
    username: str

class GetByEmail(BaseModel):
    email: EmailStr

class GetByEmailResponse(BaseResponse):
    id: UUID4
    email: EmailStr
    username: str

class ListUserResponse(BaseResponse):
    users: List[UserResponse]