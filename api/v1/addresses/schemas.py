from pydantic import BaseModel


class AddressCreate(BaseModel):
    partner_id: str
    country_id: int
    regions_id: int
    city: str
    street: str
    postal_code: str
    address_type_id: int
    is_legal_address: bool


class AddressOut(AddressCreate):
    id: int
