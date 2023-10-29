from sqlalchemy import (FetchedValue, Integer, String, Column,
                        ForeignKey, Enum, Time,
                        DateTime, Numeric, Index, event)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship, Mapped, mapped_column
# from regions.models import RegionsRussiaModel
from enum import Enum as PyEnum
from datetime import datetime

from v1.constants import weekdays_constants

from v1.config.database_conf import Base


class WeekDays(PyEnum):
    Monday = weekdays_constants.MONDAY
    Tuesday = weekdays_constants.TUESDAY
    Wednesday = weekdays_constants.WEDNESDAY
    Thursday = weekdays_constants.THURSDAY
    Friday = weekdays_constants.FRIDAY
    Saturday = weekdays_constants.SATURDAY
    Sunday = weekdays_constants.SUNDAY


class Partner(Base):
    __tablename__ = 'partners'
    # __table_args__ = {"schema": "public"}

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True)
    partner_id: Mapped[int] = Column(
        Integer, server_default=FetchedValue(), default=None)
    organization_name: Mapped[str] = mapped_column(String(255), nullable=False)
    organization_website: Mapped[str] = mapped_column(
        String(255), nullable=False)
    organization_email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    organization_phone: Mapped[str] = mapped_column(
        String(50), nullable=False, unique=True)
    hash_password: Mapped[str] = mapped_column(String(255), nullable=False)
    inn: Mapped[str] = mapped_column(String(12), nullable=False, unique=True)
    ogrn: Mapped[str] = mapped_column(String(13), nullable=False, unique=True)
    kpp: Mapped[str] = mapped_column(String(9), nullable=False, unique=True)
    organization_description: Mapped[str] = mapped_column(
        String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # relationships with partners table
    addresses_relation = relationship(
        "Address")
    contacts_relation = relationship(
        "PartnerContact")
    payment_conditions_relation = relationship(
        "PartnerPaymentCondition")
    inventory_systems_relation = relationship(
        "PartnerInventorySystem")
    schedules_relation = relationship(
        "PartnerSchedule")


Index("idx_partner_organization_email",
      Partner.organization_email, unique=True)
Index("idx_partner_organization_phone",
      Partner.organization_phone, unique=True)
Index("idx_partner_inn", Partner.inn, unique=True)
Index("idx_partner_ogrn", Partner.ogrn, unique=True)


class ManagerPosition(Base):
    __tablename__ = 'partner_manager_positions'
    # __table_args__ = {"schema": "public"}
    id = Column(Integer, primary_key=True,
                server_default=FetchedValue(), default=None)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # manager_position_relation = relationship(
    #     "PartnerContact",
    # back_populates="partner_contacts_position_relation")


class PartnerContact(Base):
    __tablename__ = 'partner_contacts'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = Column(Integer, primary_key=True,
                             server_default=FetchedValue(),
                             default=None, index=True)
    partner_id: Mapped[UUID] = Column(UUID(as_uuid=True), ForeignKey(
        'partners.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False, index=True)
    position_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'partner_manager_positions.id'), nullable=False, index=True)
    manager_organization_name: Mapped[str] = mapped_column(
        String(255), nullable=False)
    manager_organization_email: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True)
    manager_organization_phone = mapped_column(
        String(50), nullable=False, unique=True)
    additional_info: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # Definition of a one-to-many relationship with the ManagerPosition
    # partner_contacts_position_relation = relationship(
    #     "ManagerPosition", back_populates="manager_position_relation")
    # Definition of a one-to-many relationship with the Partner
    # partner_contacts_relation = relationship(
    #     "Partner", back_populates="contacts_relation")


class PartnerPaymentCondition(Base):
    __tablename__ = 'partner_payment_conditions'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = Column(Integer, primary_key=True,
                             server_default=FetchedValue(), default=None)
    partner_id: Mapped[int] = Column(UUID(as_uuid=True), ForeignKey(
        'partners.id'), nullable=False)
    payment_method_id: Mapped[int] = Column(Integer, ForeignKey(
        'public.payment_method_type.id'), nullable=False)
    acceptance_conditions: Mapped[str] = mapped_column(String)
    payment_days_deferral: Mapped[int] = mapped_column(Integer, nullable=False)
    minimum_order_cost: Mapped[float] = mapped_column(Numeric, nullable=False)
    delivery_cost: Mapped[float] = mapped_column(Numeric, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime,
                                                 nullable=False,
                                                 server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # Definition of a one-to-many relationship with
    # the PaymentMethodTypeTable model
    # partner_payment_method_type_relation = relationship(
    #     'PaymentMethodType', remote_side=id,
    #     backref="payment_method_relation")
    # Definition of a one-to-many relationship with the Partner
    # partner_payment_relation = relationship(
    #     "Partner", back_populates="payment_conditions_relation")


class PartnerInventorySystem(Base):
    __tablename__ = 'partner_inventory_systems'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = Column(Integer, primary_key=True,
                             server_default=FetchedValue(), default=None)
    partner_id = Column(UUID(as_uuid=True), ForeignKey(
        'partners.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    inventory_systems: Mapped[str] = mapped_column(String(255), nullable=False)
    price_list_file_path: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # partner_inventory_systems_relation = relationship(
    #     "Partner", back_populates="inventory_systems_relation")


class ScheduleItem(Base):
    __tablename__ = 'schedule_items'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = Column(Integer, primary_key=True,
                             server_default=FetchedValue(), default=None)
    partner_schedule_id: Mapped[int] = Column(Integer, ForeignKey(
        'partner_schedules.id', onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False)
    day_of_week: Mapped[Enum(WeekDays)] = mapped_column(
        Enum(WeekDays), nullable=False)
    start_time: Mapped[Time] = mapped_column(Time, nullable=False)
    end_time: Mapped[Time] = mapped_column(Time, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # schedule_item_relation = relationship(
    #     "PartnerSchedule", back_populates="partner_schedule_item_relation")


class PartnerSchedule(Base):
    __tablename__ = 'partner_schedules'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True,
                             server_default=FetchedValue(), default=None)
    partner_id: Mapped[int] = Column(UUID(as_uuid=True), ForeignKey(
        'partners.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    schedule_type_id: Mapped[int] = mapped_column(Integer, ForeignKey(
        'public.schedule_type.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, server_default=text("NOW()"))

    # partner_schedule_item_relation = relationship(
    #     "ScheduleItem", back_populates="schedule_item_relation")

    # Definition of a one-to-many relationship with the ScheduleTypeTable model
    # partner_schedule_type_relation = relationship(
    #     "ScheduleType", remote_side=id,
    #     backref="schedule_type_relation")

    # Definition of a one-to-many relationship with the Partner model
    # partner_schedules_relation = relationship(
    #     "Partner", back_populates="schedules_relation")


def function_updated_at(mapper, connection, target):
    target.updated_at = text("now()")


update_list = [Partner, ManagerPosition, PartnerContact,
               PartnerInventorySystem, PartnerPaymentCondition,
               ScheduleItem, PartnerSchedule]

for item in update_list:
    event.listen(item, 'before_update', function_updated_at)
