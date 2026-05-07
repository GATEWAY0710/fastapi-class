from logging import Logger

from domain.models import Role
from interface.persistence.role_repository import RoleRepository
from interface.use_case.model.base_response import BaseResponse
from interface.use_case.model.role import CreateRoleResponse, Get, GetResponse, ListResponse
from interface.use_case.role_service import RoleService as DefaultRoleService

class RoleService(DefaultRoleService):
    _logger: Logger
    _role_repository: RoleRepository

    def __init__(self, logger: Logger, role_repository: RoleRepository):
        self._logger = logger
        self._role_repository = role_repository

    async def create(self, role: Role) -> BaseResponse:
        self._logger.info(f"Creating role {role.name}")
        role_exist = await  self._role_repository.get(role.name)
        if role_exist:
            self._logger.warning(f"role {role.name} already exists ")
            response = BaseResponse(status= False, message= f"role {role.name} already exists")
            response._status_code = 400
            return response
        db_role = Role(name=role.name, description=role.description)
        db_role = await self._role_repository.create(db_role)
        if not db_role:
            self._logger.error(f"error creating role {role.name}")
            response = BaseResponse(status= False, message= f"error creating role {role.name}")
            response._status_code = 500
            return response
        self._logger.info(f"role {role.name} created")
        response = CreateRoleResponse(status=True, message= f"role {role.name} created", id=db_role.id, name=db_role.name)
        response._status_code = 200
        return response

    async  def get(self, name: str) -> BaseResponse:
        role_exist = await self._role_repository.get(name=name)
        if not role_exist:
            self._logger.warning(f"role {name} does not exist")
            response = BaseResponse(status= False, message= f"role {name} does not exist")
            response._status_code = 400
            return response
        self._logger.info(f"role {name} found")
        response = GetResponse(status=True, message= f"role {name} found", id=role_exist.id, name=role_exist.name, description=role_exist.description)
        response._status_code = 200
        return response

    async def list(self) -> BaseResponse:
        roles = await self._role_repository.list()
        role_responses = [
            CreateRoleResponse(status=True, **role_dict)
            for role_dict in roles
        ]
        self._logger.info(f"role list")
        response = ListResponse(status=True, message= f"role list", roles=role_responses)
        response._status_code = 200
        return response
