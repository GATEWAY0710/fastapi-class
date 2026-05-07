from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Depends

from api.token import allowed_roles
from interface.use_case.model.auth import TokenData
from interface.use_case.model.base_response import BaseResponse
from implementation.dependency import container
from interface.use_case.model.role import CreateRoleResponse, CreateRole, GetResponse, ListResponse
from interface.use_case.model.user import ListUserResponse

router = APIRouter()

@router.post("", response_model=CreateRoleResponse)
async def create_role(request: CreateRole, current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    role_service = container.role_service()
    response = await role_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/list", response_model=ListResponse)
async def list(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    role_service = container.role_service()
    response = await role_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{name}", response_model=GetResponse)
async def get(name: str, current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    role_service = container.role_service()
    response = await role_service.get(name)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

