from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query, Depends

from api.token import get_current_user, allowed_roles
from interface.use_case.model.auth import TokenData
from interface.use_case.model.base_response import BaseResponse
from implementation.dependency import container
from interface.use_case.model.user import CreateUser, GetByEmailResponse, GetResponse, ListUserResponse, UserResponse
from fastapi.security import HTTPBearer

security_scheme = HTTPBearer()

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create(request: CreateUser):
    user_service = container.user_service()
    response = await user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/get-by-email", response_model=GetByEmailResponse)
async def get_by_email(email: str = Query(..., description="Email of the user to fetch"), Token: str = Depends(get_current_user)):
    user_service = container.user_service()
    response = await user_service.get_by_email(email)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/list", response_model=ListUserResponse)
async def list(current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    user_service = container.user_service()
    response = await user_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{id}", response_model=GetResponse)
async def get(id: UUID, Token: str = Depends(get_current_user)):
    user_service = container.user_service()
    response = await user_service.get(id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{user_id}/roles/{role_id}", response_model=BaseResponse)
async def assign_role(user_id: str, role_id: str, current_user: Annotated[TokenData, Depends(allowed_roles(["Admin"]))]):
    user_service = container.user_service()
    response = await  user_service.assign_role(user_id, role_id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response