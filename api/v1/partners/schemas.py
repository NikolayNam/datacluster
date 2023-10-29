from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from uuid import UUID
from datetime import time
from decimal import Decimal
from enum import Enum
from v1.constants import weekdays_constants
import phonenumbers as phone


class PublicPartner(BaseModel):
    partner_id: Optional[int] = None
    organization_name: str
    organization_website: str
    organization_description: str
    organization_email: EmailStr
    organization_phone: str

    class Config:
        from_attributes = True


class PrivatePartner(PublicPartner):
    id: UUID
    inn: str
    ogrn: str
    kpp: str
    hash_password: str

    @validator("inn")
    def validate_inn(cls, inn: str):
        if len(inn) not in (10, 12):
            raise ValueError("INN must be 10 or 12 characters long")
        return inn

    @validator("ogrn")
    def validate_ogrn(cls, ogrn: str):
        if len(ogrn) not in (13, 15):
            raise ValueError("OGRN must be 13 or 15 characters long")
        return ogrn

    @validator("kpp")
    def validate_kpp(cls, kpp: str):
        if len(kpp) != 9:
            raise ValueError("KPP must be 9 characters long")
        return kpp

    @validator("organization_phone")
    def validate_organization_phone(cls, organization_phone: str):
        try:
            parsed_phone = phone.parse(organization_phone, "RU")
            if not phone.is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number")
            return phone.format_number(parsed_phone,
                                       phone.PhoneNumberFormat.E164)
        except phone.NumberParseException:
            raise ValueError("Invalid phone number")

    class Config:
        from_attributes = True


# Partner contact-related models:
class PartnerManagerPosition(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True


class PartnerManagerPositionCreate(BaseModel):
    name: str

    class Config:
        from_attributes = True


class PartnerContact(BaseModel):
    id: int
    partner: PublicPartner
    manager_organization_first_name: str
    manager_organization_second_name: str
    manager_organization_email: EmailStr
    manager_organization_phone: str
    position: PartnerManagerPosition
    additional_info: Optional[str]

    @validator('manager_organization_first_name')
    def validate_name(cls, name: str) -> str:
        if len(name) < 2:
            raise ValueError(
                "Invalid name. It should be at least 2 characters long.")
        return name

    @validator('manager_organization_email')
    def validate_email(cls, email: EmailStr) -> EmailStr:
        domain = email.split('@')[-1]
        if domain.lower() == "example.com":
            raise ValueError(
                "Invalid email domain. 'example.com' is not allowed.")
        return email

    @validator("manager_organization_phone")
    def validate_organization_phone(cls, manager_organization_phone: str):
        try:
            parsed_phone = phone.parse(manager_organization_phone, "RU")
            if not phone.is_valid_number(parsed_phone):
                raise ValueError("Invalid phone number")
            return phone.format_number(parsed_phone,
                                       phone.PhoneNumberFormat.E164)
        except phone.NumberParseException:
            raise ValueError("Invalid phone number")

    @validator('additional_info')
    def validate_additional_info(cls, info: Optional[str]) -> Optional[str]:
        if info and len(info) > 1000:
            raise ValueError(
                "Invalid additional info.It should not exceed 1000 characters."
            )
        return info

    class Config:
        from_attributes = True


# Partner payment-related models:
class PartnerPaymentCondition(BaseModel):
    id: int
    partner: PublicPartner
    acceptance_conditions: Optional[str]
    payment_method_id: int
    payment_days_deferral: int
    minimum_order_cost: Decimal
    delivery_cost: Decimal


# Partner inventory-related models:
class PartnerInventorySystem(BaseModel):
    id: int
    partner: PublicPartner
    inventory_systems: str
    price_list_file_path: str


# Partner schedule-related models:
class WeekDays(str, Enum):
    Monday = weekdays_constants.MONDAY
    Tuesday = weekdays_constants.TUESDAY
    Wednesday = weekdays_constants.WEDNESDAY
    Thursday = weekdays_constants.THURSDAY
    Friday = weekdays_constants.FRIDAY
    Saturday = weekdays_constants.SATURDAY
    Sunday = weekdays_constants.SUNDAY


class PartnerSchedule(BaseModel):
    id: int
    partner: PublicPartner
    schedule_type_id: int


class ScheduleItem(BaseModel):
    id: int
    partner_schedule: PartnerSchedule
    day_of_week: WeekDays
    start_time: time
    end_time: time
