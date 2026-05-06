from abc import ABCMeta

from interface.use_case.model.base_response import BaseResponse
from interface.use_case.model.role import CreateRole, Get


class RoleService(metaclass=ABCMeta):
    """Default class for all role service"""
    async def create(self, role: CreateRole) -> BaseResponse:
        """Create a new role"""
        raise NotImplementedError

    async def get(self, role:Get) -> BaseResponse:
        """Get a role"""
        raise NotImplementedError

    async def list(self) -> BaseResponse:
        """List all roles"""
        raise NotImplementedError