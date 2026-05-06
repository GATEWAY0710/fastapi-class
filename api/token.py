import os
from datetime import timedelta, datetime, timezone
from typing import Union, Annotated

import jwt
from jwt.exceptions import InvalidTokenError, PyJWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from implementation.dependency import container
import logging
from interface.use_case.model.auth import TokenData

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

security_key = HTTPBearer()

def create_token(data: dict, expires_delta: Union[timedelta, None]) -> tuple[str, str, datetime]:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    refresh_exp = expire + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode["exp"] = refresh_exp
    encoded_refresh_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, encoded_refresh_jwt, expire

async def get_current_user(auth: Annotated[HTTPAuthorizationCredentials, Depends(security_key)]) -> TokenData:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = auth.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(
            email=email,
            user_id=payload.get("user_id"),
            username=payload.get("username"),
            roles=payload.get("roles", [])
        )
    except InvalidTokenError:
        raise credentials_exception

    user_service = container.user_service()
    response = await user_service.get_user_by_email(email=token_data.user_id)
    if not response.status:
        raise credentials_exception

    return token_data

def allowed_roles(required_roles: list[str]):
    async def role_checker(current_user: Annotated[TokenData, Depends(get_current_user)]):
        if required_roles == []:
            return current_user
        if not any(role in current_user.roles for role in required_roles):
            logging.warning(f"user with roles {current_user.roles} tried to access a resource requiring roles {required_roles}")
            raise HTTPException(status_code=403, detail="not enough permissions")
        return current_user
    return role_checker