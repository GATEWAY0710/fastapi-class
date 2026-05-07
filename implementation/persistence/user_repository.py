from typing import Optional, List
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from domain.models import User, Role
from interface.persistence.user_repository import UserRepository as DefaultUserRepository
from logging import Logger
from implementation.database import AsyncSessionLocal

class UserRepository(DefaultUserRepository):
    _logger: Logger
    def __init__(self, logger: Logger):
        self._logger = logger

    async def create(self, user: User) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            try:
                session.add(user)
                await session.commit()
                await session.refresh(user)
                self._logger.info(f"user with id {user.id} was created")
                return user
            except Exception as e:
                await session.rollback()
                self._logger.error(f"an error occurred while creating user {user.id}, {e}")
                return None


    async def get(self, id: UUID) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            try:
                statement = (
                    select(User)
                    .options(joinedload(User.roles))
                    .where(User.id == str(id))
                )
                result = await session.execute(statement)
                user = result.unique().scalars().one_or_none()
                return user
            except Exception as e:
                self._logger.error(f"an error occurred while getting user {id}, {e}")
                return None


    async def update(self, user: User) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            try:
                statement = (
                    select(User).where(User.id == str(user.id))
                )
                result = await session.execute(statement)
                db_user = result.scalars().one_or_none()
                if db_user is None:
                    self._logger.error(f"unable to find user with id {user.id} to update")
                    return None
                db_user.hash_salt = user.hash_salt
                db_user.password_hash = user.password_hash
                db_user.modified_at = user.modified_at
                db_user.username = user.username
                db_user.modified_by = user.modified_by

                await session.commit()
                await session.refresh(db_user)
                return db_user
            except Exception as e:
                await session.rollback()
                self._logger.error(f"an error occurred while updating user {user.id}, {e}")
                return None


    async def get_by_email(self, email: str) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            try:
                statement = (
                    select(User)
                    .options(joinedload(User.roles))
                    .where(User.email == email)
                )
                result = await session.execute(statement)
                user = result.unique().scalars().one_or_none()
                return user
            except Exception as e:
                self._logger.error(f"an error occurred while getting user {email}, {e}")
                return None

    async def list(self) -> List[User]:
        async with AsyncSessionLocal() as session:
            try:
                result = await session.execute(select(User))
                return list(result.scalars().all())
            except Exception as e:
                self._logger.error(f"an error occurred while listing users {e}")
                return []


    async def assign_role(self, user_id: UUID, role_id: UUID) -> Optional[User]:
        async with AsyncSessionLocal() as session:
            try:
                statement_user = (
                    select(User).options(joinedload(User.roles)).where(User.id == str(user_id))
                )
                result_user = await session.execute(statement_user)
                user = result_user.unique().scalars().one_or_none()

                statement_role = (
                    select(Role).where(Role.id == str(role_id))
                )
                result_role = await session.execute(statement_role)
                role = result_role.scalars().one_or_none()

                if not user or not role:
                    self._logger.error(f"Either user with id {user_id} or role with id {role_id} does not exist")
                    return None

                if role not in user.roles:
                    user.roles.append(role)
                    await session.commit()
                    await session.refresh(user)
                return user
            except Exception as e:
                await session.rollback()
                self._logger.error(f"Error assigning role, {e}")
                return None
