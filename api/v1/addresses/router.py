from typing import List

from fastapi import APIRouter, Depends
# partners
from v1.addresses.models import Address as Address_model
from v1.addresses.schemas import AddressOut
from sqlalchemy.ext.asyncio import AsyncSession
from v1.config.database_conf import get_db
from v1.utils.db_utils import (find_all_instances, find_instance)

address_router = APIRouter(prefix="/address")


@address_router.get("/{address_id}", response_model=AddressOut)
async def get_public_partner(address_id: int,
                             db_session: AsyncSession = Depends(get_db)):
    partner_address = await find_instance(
        db_session,
        Address_model,
        Address_model.id == address_id,
        f"There is no record for requested address ID value: {address_id}",
    )
    return AddressOut.from_orm(partner_address)


@address_router.get("/", response_model=List[AddressOut])
async def get_public_partners(db_session: AsyncSession = Depends(get_db)):
    partner_address_all = await find_all_instances(
        db_session,
        Address_model,
        f'{"Partners address not found"}'
    )
    return List[AddressOut.from_orm(partner_address_all)]
