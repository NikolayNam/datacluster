from fastapi import APIRouter, Depends, status
from v1.config.database_conf import get_db
from v1.auth.models import User
from v1.auth.schemas import UserAuth, Token
from v1.utils.db_utils import check_multiple_conditions_and
from v1.utils.db_utils import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Form
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse, Response, JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.models import OAuthFlowImplicit
from fastapi.requests import Request
from typing import Annotated
import uuid
import httpx
import base64
import os

auth_router = APIRouter(prefix="/api/v1/auth")


@auth_router.get("/yandex")
def auth_yandex():
    client_id = os.environ.get("YandexClientId")
    redirect = f'https://oauth.yandex.ru/authorize?response_type=code&client_id={client_id}'
    return RedirectResponse(redirect, status_code=302)


@auth_router.get("/yandex/token")
async def auth_yandex_info(code: str):
    content = {
        'grant_type': 'authorization_code',
        'code': code,
    }

    async with httpx.AsyncClient() as client:

        url_token = "https://oauth.yandex.ru/token"

        ClientId_bytes = bytes(os.environ.get("YandexClientId"), 'utf-8')
        ClientSecret_bytes = bytes(
            os.environ.get("YandexClientSecret"), 'utf-8')

        encoded = base64.b64encode(ClientId_bytes + b':' + ClientSecret_bytes)

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic ' + encoded
        }

        response = await client.post(url_token, data=content, headers=headers)

        try:

            response_json = response.json()
            access_token = response_json['access_token']

            url_info = 'https://login.yandex.ru/info?'

            headers.update({'Authorization': f'OAuth {access_token}'})

            response_info = await client.get(url_info, headers=headers)

            response_info_json = response_info.json()

        except Exception as e:

            print(e)

    return response_info_json


@auth_router.get("/yandex/info")
async def info_user_yandex(code: str):
    content = {
        'grant_type': 'authorization_code',
        'code': code,
        # 'client_id':  os.environ.get("YandexClientId"),
        # 'client_secret': os.environ.get("YandexClientSecret")
    }
    async with httpx.AsyncClient() as client:

        url = "https://login.yandex.ru/info?"

        ClientId_bytes = bytes(os.environ.get("YandexClientId"), 'utf-8')
        ClientSecret_bytes = bytes(
            os.environ.get("YandexClientSecret"), 'utf-8')

        encoded = base64.b64encode(ClientId_bytes + b':' + ClientSecret_bytes)

        headers = {
            'Content-type': 'application/x-www-form-urlencoded',
            'Authorization': b'Basic ' + encoded
        }

        response = await client.post(url, data=content, headers=headers)
        try:
            response_json = response.json()
            access_token = response_json['access_token']
        except Exception as e:
            print(e)

    return response_json


@auth_router.post('/signup', summary="Create new user")
async def create_user(user: UserAuth,
                      db_session: AsyncSession = Depends(get_db)):

    # querying database to check if user already exist
    conditions_or_email = [
        User.phone == user.phone,
        User.email == user.email,
        User.status is True
    ]

    if await check_multiple_conditions_and(db_session, User, *conditions_or_email):
        raise HTTPException(
            status_code=400,
            detail="User with this email or phone already exist")

    # Generate a UUID for the new partner
    new_user_id = uuid.uuid4()

    print(user)
    new_user = User(id=new_user_id,
                    email=user.email,
                    phone=user.phone,
                    password=generate_password_hash(user.password),
                    status=False)

    try:
        # Insert the new partner into the database
        db_session.add(new_user)
        await db_session.flush()

        # Create a PrivatePartner instance
        # using the data from the created partner
        created_user = UserAuth(**new_user.__dict__)

        # returned created user models
        return created_user

    except IntegrityError as ie:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ie))

    except TypeError as te:
        db_session.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(te))
