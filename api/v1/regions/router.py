from fastapi import APIRouter, Depends
from v1.regions.models import (RegionsRussiaModel)
from v1.regions.schemas import (RegionsRussiaSchema)
from v1.utils.db_utils import find_instance, find_all_instances
from v1.config.database_conf import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

regions_router = APIRouter(prefix="/regions")


@regions_router.get("/{region_id}", response_model=RegionsRussiaSchema)
async def get_region_russia(region_id: int,
                            db_session: AsyncSession = Depends(get_db)):
    regions_one = await find_instance(
        db_session,
        RegionsRussiaModel,
        RegionsRussiaModel.id == region_id,
        f"There is no record for requested regions ID value: {region_id}",
    )
    return RegionsRussiaSchema.from_attributes(regions_one)


@regions_router.get("/", response_model=List[RegionsRussiaSchema])
async def get_regions_russia(db_session: AsyncSession = Depends(get_db)):
    regions_all = await find_all_instances(
        db_session,
        RegionsRussiaModel,
        f'{"Regions not found"}'
    )
    return [RegionsRussiaSchema.from_attributes(region) for region in regions_all]
