from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class AddressList(str, Enum):
    Legal = 'Legal'
    Actual = 'Actual'


class PaymentMethodList(str, Enum):
    Cash = 'Cash'
    Non_Cash = 'Non_Cash'


class ScheduleList(str, Enum):
    Delivery = 'Delivery'
    Self_Delivery = 'Self_Delivery'


class AddressType(BaseModel):
    id: int
    name: AddressList
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PaymentMethodType(BaseModel):
    id: int
    name: PaymentMethodList
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScheduleType(BaseModel):
    id: int
    name: ScheduleList
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
