from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, HTTPException, Query
from interface.use_case.model.base_response import BaseResponse
from implementation.dependency import container
from interface.use_case.model.user import CreateUser, GetByEmailResponse, GetResponse, ListUserResponse, UserResponse

# --- STUDENT LESSON: NO AUTHORIZATION ---
# This controller is a duplicate of the user controller, but with all
# "Depends(get_current_user)" or "allowed_roles" removed.
# This makes it completely public.

router = APIRouter()

@router.post("", response_model=UserResponse)
async def create(request: CreateUser):
    user_service = container.user_service()
    response = await user_service.create(request)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/filter", response_model=GetByEmailResponse)
async def get_by_email(email: str = Query(..., description="Email of the user to fetch")):
    user_service = container.user_service()
    response = await user_service.get_by_email(email)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/list-all", response_model=ListUserResponse)
async def list():
    # Anyone can see the list! No token needed.
    user_service = container.user_service()
    response = await user_service.list()
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response

@router.get("/{id}", response_model=GetResponse)
async def get(id: UUID):
    user_service = container.user_service()
    response = await user_service.get(id)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    return response
