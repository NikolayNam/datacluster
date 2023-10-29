from pydantic import BaseModel, EmailStr
from typing import List
from uuid import UUID
from datetime import datetime


class UserRoleBase(BaseModel):
    role: str


class UserRoleCreate(UserRoleBase):
    pass


class UserRole(UserRoleBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str
    fullname: str
    created_on: datetime
    status: bool


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: UUID
    roles: List[UserRole] = []

    class Config:
        from_attributes = True
