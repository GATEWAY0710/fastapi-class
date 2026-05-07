from logging import Logger
from typing import Optional, List

from sqlalchemy import select

from implementation.database import AsyncSessionLocal
from domain.models import Role
from interface.persistence.role_repository import RoleRepository as DefaultRoleRepository
from interface.use_case.model.role import Get


class RoleRepository(DefaultRoleRepository):
    _logger: Logger

    def __init__(self, logger: Logger):
        self._logger = logger

    async def create(self, role: Role) -> Optional[Role]:
        async with AsyncSessionLocal() as session:
            try:
                session.add(role)
                await session.commit()
                await session.refresh(role)
                self._logger.info(f"role with id {role.id} created")
                return role
            except Exception as e:
                await session.rollback()
                self._logger.error(f"role with id {role.id} failed", {e})
                return None

    async def get(self, name: str) -> Optional[Role]:
        async with AsyncSessionLocal() as session:
            try:
                statement = (
                    select(Role).where(Role.name == name)
                )
                result = await session.execute(statement)
                role = result.scalars().one_or_none()
                return role
            except Exception as e:
                self._logger.error(f"role with id {role.id} failed to retrive", {e})
                return None

    async def list(self) -> List[Role]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(select(Role))
                roles = result.scalars().all()
                return [
                    {"id" : str(u.id), "name" : u.name, "description" : u.description}
                    for u in roles
                ]
            except Exception as e:
                self._logger.error(f"role list failed", {e})
                return []