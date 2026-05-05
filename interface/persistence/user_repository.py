from abc import ABCMeta
from typing import Optional, List
from uuid import UUID

from domain.models import User


class UserRepository(metaclass=ABCMeta):
    """Default class for user repository"""
    async def create(self, user: User) -> Optional[User]:
        """Create new user"""
        raise NotImplementedError

    async def get(self, id: UUID) -> Optional[User]:
        """Get user by id"""
        raise NotImplementedError

    async def update(self, user: User) -> Optional[User]:
        """Update user"""
        raise NotImplementedError

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        raise NotImplementedError

    async def list(self) -> List[User]:
        """List all users"""
        raise NotImplementedError

    async def assign_role(self, user_id: UUID, role_id: UUID) -> Optional[User]:
        """Assign role to user"""
        raise NotImplementedError