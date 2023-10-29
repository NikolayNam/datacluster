from sqlalchemy import (Integer, String, Column,
                        Boolean, ForeignKey, DateTime)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
from sqlalchemy.orm import Mapped, mapped_column
# from regions.models import RegionsRussiaModel
from datetime import datetime


from v1.config.database_conf import Base


class Address(Base):
    __tablename__ = 'partner_addresses'
    # __table_args__ = {"schema": "public"}
    id: Mapped[int] = mapped_column(primary_key=True)
    partner_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey(
        'partners.id',
        onupdate="CASCADE",
        ondelete="CASCADE"),
        nullable=False,
        index=True)
    # nullable=False)
    # country_id -country field from country tables
    # country_id = mapped_column(Integer,
    # ForeignKey('countries.id'), nullable=False)
    # The unmentioned fields can be added in the future if needed.
    regions_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('regions_russia.id'),
        nullable=False)
    # city - city(format "city_name")
    city: Mapped[str] = mapped_column(String,
                                      nullable=False)
    # street - street and house number
    street: Mapped[str] = mapped_column(String,
                                        nullable=False)
    # postal_code - postal code in Russia (numeric) in USA (alphanumeric)
    postal_code: Mapped[str] = mapped_column(String,
                                             nullable=False)
    # address_type - (Legal[1] - Legal , Actual[2] - Actual address)
    address_type_id: Mapped[int] = Column(
        Integer,
        ForeignKey('address_type.id'),
        nullable=False)
    # Legal address [True or False]
    is_legal_address: Mapped[bool] = mapped_column(Boolean,
                                                   nullable=False)

    # systems field create [datetime]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("NOW()")
    )
    # systems field update [datetime]
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=text("NOW()"))

    # partner_address = mapped_column(String, nullable=False)
    # - it' s legacy field
    # apartment = mapped_column(String, nullable=False) - it' s legacy field
    # building = mapped_column(String) - it' s legacy field
    # state_id = mapped_column(String, nullable=False) - it' s legacy field
    # # Definition of a one-to-many relationship with the Partner model
    # partner_address_relation = relationship(
    #     "Partner")
    # partner_address_type_relation = relationship(
    #     "AddressType", back_populates="address_type_relation")
    # # Definition of a one-to-many relationship with the RegionsRussiaModel
    # partner_region = relationship(
    #     RegionsRussiaModel)
