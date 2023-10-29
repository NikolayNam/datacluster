# security.py
import os
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from datetime import timedelta
from fastapi import FastAPI

app_env = os.environ.get("APP_ENV", "development")

origins_production = os.environ.get("ORIGINS").split(',')
origins_local = os.environ.get("ORIGINS_LOCAL").split(',')

if app_env == "production":
    ssl_keyfile = "/etc/nginx/ssl/datacluster/datacluster.key"
    ssl_certfile = "/etc/nginx/ssl/datacluster/datacluster.crt"
    https_only_check = True
    origins = origins_production
elif app_env == "development":
    ssl_keyfile = None
    ssl_certfile = None
    https_only_check = False
    origins = origins_local


def setup_security(app: FastAPI):

    app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=os.environ.get("SECRET_KEY_API"),
        max_age=timedelta(minutes=1440),
        https_only=https_only_check,
    )
