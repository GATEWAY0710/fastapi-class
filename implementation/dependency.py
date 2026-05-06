from dependency_injector import containers, providers
from typing import Callable
from interface.persistence.user_repository import UserRepository as DefaultUserRepository
from interface.persistence.role_repository import RoleRepository as DefaultRoleRepository

from implementation.persistence.user_repository import UserRepository
from implementation.persistence.role_repository import RoleRepository

from interface.use_case.user_service import UserService as DefaultUserService
from interface.use_case.role_service import RoleService as DefaultRoleService

from implementation.use_case.user_service import UserService
from implementation.use_case.role_service import RoleService

import logging
logger = logging.getLogger(__name__)

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    user_repository : Callable[[], DefaultUserRepository] = providers.Factory(UserRepository, logger=logger)
    user_service: Callable[[], DefaultUserService] = providers.Factory(UserService, user_repository=user_repository ,logger=logger)

    role_repository: Callable[[], DefaultRoleRepository] = providers.Factory(RoleRepository, logger=logger)
    role_service: Callable[[], DefaultRoleService] = providers.Factory(RoleService, logger=logger, role_repository=role_repository)


container = Container()