from __future__ import annotations
import datetime
from typing import Optional, List

from sqlalchemy import CHAR, String, DateTime, func, Table, Column, ForeignKey, UniqueConstraint, Enum, Index
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from uuid import UUID as UUID_T, uuid4
from domain.enum.role import  Role as DomainRole
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    __tablename__ : str = None

    id : Mapped[UUID_T] = mapped_column(CHAR(36), primary_key= True , default= uuid4)
    created_by: Mapped[Optional[str]] = mapped_column(String(50))
    modified_by: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    modified_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), server_default=func.now())

user_roles = Table('user_roles',
                   Base.metadata,
                   Column('user_id', ForeignKey('users.id'), primary_key= True),
                   Column('role_id', ForeignKey('roles.id'), primary_key= True),
)

class User(BaseModel):
    __tablename__ = 'users'
    __table_args__ = (
        Index("ix_users_username", "username"),
        UniqueConstraint("email", name="unique_users_email"),
    )

    email: Mapped[str] = mapped_column(String(50), nullable=False)
    username: Mapped[str] = mapped_column(String(50))
    hash_salt: Mapped[str] = mapped_column(String(1000), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(1000), nullable=False)

    profile: Mapped[Optional["Profile"]] = relationship(back_populates="user", uselist=False, cascade="all, delete-orphan")
    roles: Mapped[List["Role"]] = relationship(secondary=user_roles, back_populates="users")


class Role(BaseModel):
    __tablename__ = 'roles'

    name: Mapped[DomainRole] = mapped_column(Enum("Admin", "User", "Manager", name= "domainrole"))
    description: Mapped[Optional[str]] = mapped_column(String(1000))
    users: Mapped[List[User]] = relationship(
        secondary=user_roles,
        back_populates="roles",
    )

class Profile(BaseModel):
    __tablename__ = 'profiles'
    __table_args__ = (
        UniqueConstraint("user_id", name="uq_profile_user_id"),
        Index("ix_profile_phone_number", "phone_number")
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable= False)
    last_name: Mapped[str] = mapped_column(String(100), nullable= False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable= False)
    middle_name: Mapped[Optional[str]] = mapped_column(String(100))

    user_id: Mapped[UUID_T] = mapped_column(CHAR(36), ForeignKey("users.id"), unique= True, nullable= False)
    user: Mapped[User] = relationship(back_populates="profile")