from abc import ABCMeta
from typing import Optional, List

from domain.models import Role


class RoleRepository(metaclass=ABCMeta):
    """default class for role repository"""
    async def create(self, role: Role) -> Optional[Role]:
        """create new role object"""
        raise NotImplementedError

    async def get(self, name: str) -> Optional[Role]:
        """get role by name"""
        raise NotImplementedError

    async def list(self)-> List[Role]:
        """list all roles"""
        raise NotImplementedError