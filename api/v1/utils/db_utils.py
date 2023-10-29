# db_utils.py

import jwt
import bcrypt

from typing import Type, Optional, List
from fastapi import HTTPException, status
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta, selectinload


class JWTException(HTTPException):
    def __init__(self, status_code: int, detail: str = None):
        super().__init__(status_code=status_code, detail=detail)


async def find_instance(
    db_session: AsyncSession,
    model: Type[DeclarativeMeta],
    condition,
    error_message: str,
):
    query = select(model).where(condition)
    result = await db_session.execute(query)
    instance = result.scalars().first()

    if instance is None:
        raise HTTPException(
            status_code=404,
            detail={"Record not found": error_message},
        )
    else:
        return instance


async def find_all_instances(
    db_session: AsyncSession,
    model: Type[DeclarativeMeta],
    error_message: str,
) -> List:
    query = select(model)
    result = await db_session.execute(query)
    instances = result.scalars().all()

    if not instances:
        raise HTTPException(
            status_code=404,
            detail={"Records not found": error_message},
        )
    else:
        return instances


async def exist(
    db_session: AsyncSession,
    model: Type[DeclarativeMeta],
    condition,
) -> bool:
    query = select(model).where(condition)
    result = await db_session.execute(query)
    exist = result.scalars().first()

    return bool(exist)


async def check_multiple_conditions(
    db_session: AsyncSession,
    model: Type[DeclarativeMeta],
    *conditions,
) -> bool:
    query = select(model).where(or_(*conditions))
    result = await db_session.execute(query)
    exist = result.scalars().first()

    return bool(exist)


async def check_multiple_conditions_and(
    db_session: AsyncSession,
    model: Type[DeclarativeMeta],
    *conditions,
) -> bool:
    query = select(model).where(and_(*conditions))
    result = await db_session.execute(query)
    exist = result.scalars().first()

    return bool(exist)


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, "your-secret-key", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise JWTException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired")
    except jwt.InvalidTokenError:
        raise JWTException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return payload

# single instance of the given model that matches the provided conditions.


async def get_one(db_session: AsyncSession,
                  model: Type, *conditions) -> Optional[object]:
    stmt = select(model).where(and_(*conditions)).options(selectinload('*'))
    result = await db_session.execute(stmt)
    return result.scalars().first()

# Password hash generation


def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# Password hash verification


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'),
                          hashed_password.encode('utf-8'))
