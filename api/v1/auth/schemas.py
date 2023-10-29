from pydantic import BaseModel, EmailStr, SecretStr, validator
from email_validator import validate_email, EmailNotValidError
from typing import Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
from enum import Enum
import re
from v1.constants import weekdays_constants
import phonenumbers as phone
import os


class UserBase(BaseModel):
    id: UUID
    user_id: int | None = None
    email: str | None
    phone: str | None
    password: str
    created_on: datetime = datetime.now()
    updated_on: datetime = datetime.now()

    @validator("phone")
    def validate_user_phone(cls, user_phone: str | None):

        if len(user_phone) == 0:
            return ''
        try:
            parsed_phone = phone.parse(user_phone, "RU")

            if not phone.is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number")
            return phone.format_number(parsed_phone, phone.PhoneNumberFormat.E164)
        except phone.NumberParseException:
            raise ValueError("Invalid phone number")

    @validator("email")
    def validate_user_email(cls, user_email: str):
        if len(user_email) == 0:
            return ''
        try:
            # replace with normalized form
            v = validate_email(user_email)
            email = v["email"]
            return email
        except EmailNotValidError as e:
            print(str(e))

    @validator("phone", "email")
    def check_len(cls, values):
        user_phone = values.get('phone')
        user_email = values.get('email')
        if user_phone is None and user_email is None:
            raise ValueError('phone and email is empty')
        return values


class Token(BaseModel):
    grant_type: str | None = 'authorization_code'
    client_id: str | None = os.environ.get("YandexClientId")
    client_secret: str | None = os.environ.get("YandexClientSecret")
    code: str | None


class UserAuth(UserBase):
    pass

    class Config:
        from_attributes = True
