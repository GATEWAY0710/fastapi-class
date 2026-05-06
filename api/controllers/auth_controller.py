from pydantic import BaseModel
from interface.use_case.model.auth import TokenResponse
from fastapi import APIRouter, Depends, HTTPException, status, Body
from interface.use_case.model.user import UserResponse, GetByEmailResponse
from implementation.dependency import container
from api.token import create_token

class TokenRequest(BaseModel):
    email: str
    password: str

router = APIRouter()

@router.post("/token", response_model=TokenResponse)
async def token(request: TokenRequest = Body()):
    user_service = container.user_service()
    response = await user_service.authenticate(request.email, request.password)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)

    response: UserResponse = await container.user_service().get_by_email(request.email)
    if not response.status:
        raise HTTPException(status_code=response._status_code, detail=response.message)
    email = response.email
    user_id = response.id
    username = response.username

    data = {
        "sub": email,
        "user_id": str(user_id),
        "username": username,
        "roles": [role.name for role in response.roles]
    }

    access_token, refresh_token, expire = create_token(data, expires_delta=None)

    return TokenResponse(
        status= True,
        message= "token generated successfully",
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="Bearer",
        expires_in=int(expire.timestamp())
    )