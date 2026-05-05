from abc import ABCMeta
from uuid import UUID

from interface.use_case.model.base_response import BaseResponse
from interface.use_case.model.user import CreateUser


class UserService(metaclass=ABCMeta):
    """Default class for the user service"""

    async  def create(self, user: CreateUser) -> BaseResponse:
        """Create new user"""
        raise NotImplementedError

    async def get(self, id: UUID) -> BaseResponse:
        """Get user by id"""
        raise NotImplementedError

    async def get_by_email(self, email: str) -> BaseResponse:
        """Get user by email"""
        raise NotImplementedError

    async def list(self):
        """List all users"""
        raise NotImplementedError

    async def assign_role(self, user_id: UUID, role_id: UUID) -> BaseResponse:
        """Assign role to user"""
        raise NotImplementedError

    async def authenticate(self, email: str, password: str) -> BaseResponse:
        """Authenticate user"""
        raise NotImplementedError