from fastapi import APIRouter, Depends
from v1.tables_type.models import (AddressType as address_type_model,
                                   PaymentMethodType as payment_method_model,
                                   ScheduleType as schedule_type_model)
from v1.tables_type.schemas import (AddressType as address_type,
                                    PaymentMethodType as payment_method_type,
                                    ScheduleType as schedule_type,)
from v1.utils.db_utils import find_all_instances

from v1.config.database_conf import get_db
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

tables_type_router = APIRouter(prefix="/tables_type")


@tables_type_router.get("/address_type",
                        response_model=List[address_type])
async def get_address_type(db_session: AsyncSession = Depends(get_db)):
    names = await find_all_instances(
        db_session,
        address_type_model,
        "Address type not found"
    )
    return [address_type.from_attributes(name) for name in names]


@tables_type_router.get("/payment_method_type",
                        response_model=List[payment_method_type])
async def get_payment_method_type(db_session: AsyncSession = Depends(get_db)):
    names = await find_all_instances(
        db_session,
        payment_method_model,
        "Payment method type not found"
    )
    return [payment_method_type.from_attributes(name) for name in names]


@tables_type_router.get("/schedule_type",
                        response_model=List[schedule_type])
async def get_schedule_type(db_session: AsyncSession = Depends(get_db)):
    names = await find_all_instances(
        db_session,
        schedule_type_model,
        f'{"Schedule type not found"}'
    )
    return [schedule_type.from_attributes(name) for name in names]
