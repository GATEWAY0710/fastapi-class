from typing import List
from pydantic import BaseModel, UUID4
from interface.use_case.model.base_response import BaseResponse

class CreateRole(BaseModel):
    name: str
    description: str

class CreateRoleResponse(BaseResponse):
    id: UUID4
    name: str

class Get(BaseModel):
    name: str

class GetResponse(BaseResponse):
    id: UUID4
    name: str
    description: str

class ListResponse(BaseResponse):
    roles: List[CreateRoleResponse]