from __future__ import annotations
from v1.config.database_conf import Base
from v1.tables_type.schemas import AddressList, PaymentMethodList, ScheduleList
from sqlalchemy import FetchedValue, Integer, Enum, DateTime, Column
from sqlalchemy.sql import text
from datetime import datetime

# from v1.constants import (address_constants, payment_constants,
#                            schedule_constants, weekdays_constants)


# class WeekDays(enum.Enum):
#     Monday = weekdays_constants.MONDAY
#     Tuesday = weekdays_constants.TUESDAY
#     Wednesday = weekdays_constants.WEDNESDAY
#     Thursday = weekdays_constants.THURSDAY
#     Friday = weekdays_constants.FRIDAY
#     Saturday = weekdays_constants.SATURDAY
#     Sunday = weekdays_constants.SUNDAY


# class AddressEnum(enum.Enum):
#     Legal = address_constants.LEGAL_ADDRESS
#     Actual = address_constants.ACTUAL_ADDRESS


# class PaymentMethodEnum(enum.Enum):
#     Cash = payment_constants.CASH_PAYMENT
#     Non_Cash = payment_constants.NON_CASH_PAYMENT


# class ScheduleEnum(enum.Enum):
#     Delivery = schedule_constants.DELIVERY
#     Self_Delivery = schedule_constants.SELF_DELIVERY


# class BaseModel(Base):
#    @declared_attr
#    def __tablename__(cls):
#        return cls.__name__.lower()

class AddressType(Base):
    __tablename__ = 'address_type'
    # __table_args__ = {'schema': 'public'}
    id: int = Column(Integer, primary_key=True,
                     server_default=FetchedValue(), default=None)
    name: str = Column(
        Enum(AddressList), nullable=False, unique=True)
    created_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # The definition of reference to the PartnerAddress model
    # address_type_relation = relationship('Address')
    # address_type_relation = relationship(
    #   "AddressTypeTable", backref=backref("address_type", remote_side=[id]))
    # address_type_relation: Mapped[List["Address"]
    #                              ] = relationship(back_populates="addresses")


class PaymentMethodType(Base):
    __tablename__ = 'payment_method_type'
    # __table_args__ = {'schema': 'public'}
    id: int = Column(Integer, primary_key=True,
                                    server_default=FetchedValue(), default=None)
    name: str = Column(
        Enum(PaymentMethodList), nullable=False, unique=True)
    created_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # The definition of reference to the PartnerAddress model

    # payment_method_relation = relationship(
    #   'PartnerPaymentCondition',
    #   back_populates='partner_payment_method_type_relation')


class ScheduleType(Base):
    __tablename__ = 'schedule_type'
    # __table_args__ = {'schema': 'public'}
    id: int = Column(Integer, primary_key=True,
                                    server_default=FetchedValue(), default=None)
    name: str = Column(
        Enum(ScheduleList), nullable=False, unique=True)
    created_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: datetime = Column(
        DateTime, nullable=False, server_default=text("NOW()"))
    # schedule_type_relation = relationship(
    #   "PartnerSchedule", back_populates="partner_schedule_type_relation")
