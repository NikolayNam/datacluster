from fastapi import APIRouter
import os

users_router = APIRouter(prefix="/users")

# Get database connection credentials from environment variables
AUTHORIZATION_BASE_URL = os.environ.get("AUTHORIZATION_BASE_URL")
TOKEN_URL = os.environ.get("TOKEN_URL")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REFRESH_URL = os.environ.get("REFRESH_URL")
REDIRECT_URL_DEV = os.environ.get("REDIRECT_URL_DEV")
REDIRECT_URL_PROD = os.environ.get("REDIRECT_URL_PROD")
SCOPES = os.environ.get("SCOPES")
