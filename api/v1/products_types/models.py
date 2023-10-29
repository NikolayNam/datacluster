from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from v1.config.database_conf import Base


class ProductTypeSchema(Base):
    __tablename__ = 'products_types'

    product_type_code: Mapped[UUID] = mapped_column(UUID)
    product_type: Mapped[str] = mapped_column(String(225))
    product_type_name: Mapped[str] = mapped_column(String(225))
    product_type_id: Mapped[int] = mapped_column(primary_key=True)
    
    product_type_tree = relationship("ProductTypeTreeSchema",
                                     back_populates="product_type_rel")


class ProductTypeTreeSchema(Base):
    __tablename__ = 'products_types_tree'

    uid: Mapped[int] = mapped_column(primary_key=True)
    product_type_id: Mapped[int] = mapped_column(ForeignKey(
        'products_types.product_type_id'))
    product_type_parent_id: Mapped[int]
    product_type_rel = relationship("ProductTypeSchema",
                                    back_populates="product_type_tree",
                                    foreign_keys=[product_type_id])
