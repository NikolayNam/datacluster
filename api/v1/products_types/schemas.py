from pydantic import BaseModel
from uuid import UUID


class ProductType(BaseModel):
    product_type_code: UUID
    product_type: str
    product_type_name: str
    product_type_id: int

    class Config:
        from_attributes = True


class ProductTypeTree(BaseModel):
    product_type: str
    product_type_id: int
    product_type_parent_id: int | None

    class Config:
        from_attributes = True


class ProductTypeFrontend(BaseModel):
    id: UUID
    name: str
    parent_id: int
    src_name: str

    class Config:
        from_attributes = True
