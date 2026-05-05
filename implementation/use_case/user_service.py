from uuid import UUID

from domain.models import User
from implementation.hashing import HashingService
from interface.persistence.user_repository import UserRepository
from interface.use_case.model.base_response import BaseResponse
from interface.use_case.model.user import CreateUser, UserResponse, GetResponse, GetByEmail, GetByEmailResponse, \
    ListUserResponse
from interface.use_case.user_service import UserService as DefaultUserService
from logging import Logger
class UserService(DefaultUserService):
    _logger: Logger
    _user_repository: UserRepository

    def __init__(self,logger:Logger,  user_repository: UserRepository):
        self._logger = logger
        self._user_repository = user_repository

    async def create(self, user: CreateUser) -> BaseResponse:
        self._logger.info(f"Creating user {user.email}")
        existing_user = await self._user_repository.get_by_email(email=user.email)
        if existing_user:
            self._logger.warning(f"User already exists")
            response = BaseResponse(status=False, message="User already exists")
            response._status_code = "400"
            return response

        if not user.validate_password():
            self._logger.warning(f"password does not match")
            response = BaseResponse(status=False, message="password does not match")
            response._status_code = "400"
            return response

        hash_salt, password_hash = HashingService().hash_password(user.password)

        if user.username is None:
            user.username = user.email

        db_user = User(
            email=user.email,
            username=user.username,
            password_hash=password_hash,
            hash_salt=hash_salt,
        )

        db_user = await self._user_repository.create(db_user)
        if not db_user:
            self._logger.error(f"Failed to create user {user.email}")
            response = BaseResponse(status=False, message="Failed to create user")
            response._status_code = "500"
            return response

        self._logger.info(f"Created user {user.email} successfully")
        response = UserResponse(status=True, message="Successfully created user", id=db_user.id, email=db_user.email, username=db_user.username)
        response._status_code = "201"
        return response

    async def get(self, id: UUID) -> BaseResponse:
        user_exist = await self._user_repository.get(id=id)
        if not user_exist:
            self._logger.warning(f"User with {id} does not exist")
            response = BaseResponse(status=False, message="User does not exist")
            response._status_code = "400"
            return response

        self._logger.info(f"User with {id} retrived successfully")
        response = GetResponse(status=True, message="Successfully retrieved user", id=user_exist.id, email=user_exist.email, username=user_exist.username)
        response._status_code = "201"
        return response


    async def get_by_email(self, email: GetByEmail) -> BaseResponse:
        user_exist = await self._user_repository.get_by_email(email=email.email)
        if not user_exist:
            self._logger.warning(f"User with {email.email} does not exist")
            response = BaseResponse(status=False, message="User does not exist")
            response._status_code = "400"
            return response

        self._logger.info(f"User with {email.email} retrived successfully")
        response = GetByEmailResponse(status=True, message="Successfully retrieved user", id=user_exist.id, email=user_exist.email, username=user_exist.username)
        response._status_code = "201"
        return response


    async def list(self) -> BaseResponse:
        users = await self._user_repository.list()

        user_responses = []
        for user in users:
            user_response = UserResponse(status=True, id=user.id, email=user.email, username=user.username)
            user_responses.append(user_response)
        self._logger.info(f"Users with {len(users)} users retrived successfully")
        response = ListUserResponse(status=True, message="Successfully retrieved users", users=user_responses)
        response._status_code = "201"
        return response

    async def assign_role(self, user_id: UUID, role_id: UUID) -> BaseResponse:
        self._logger.info(f"Assigning role {role_id} to user {user_id}")
        user = await self._user_repository.assign_role(user_id=user_id, role_id=role_id)
        if not user:
            self._logger.error(f"failed to assign role {role_id} to user {user_id}")
            response = BaseResponse(status=False, message="Failed to assign role")
            response._status_code = "500"
            return response
        self._logger.info(f"Successfully assigned role {role_id} to user {user_id}")
        response = BaseResponse(status=True, message="Successfully assigned role")
        response._status_code = "201"
        return response

    async def authenticate(self, email: str, password: str) -> BaseResponse:
        user = await self._user_repository.get_by_email(email=email)
        if not user:
            response = BaseResponse(status=False, message="invalid email or password")
            response._status_code = "400"
            return response
        if not HashingService().validate_password(password, user.password_hash, user.hash_salt):
            response = BaseResponse(status=False, message="invalid email or password")
            response._status_code = "400"
            return response

        return BaseResponse(status=True, message="user Successfully authenticated")