from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from uuid import uuid4

# regions
from v1.regions.models import (RegionsRussiaModel)

# partners
from v1.partners.models import (Partner)
from v1.partners.schemas import (PublicPartner, PrivatePartner)
from v1.utils.db_utils import (find_instance, exist, check_multiple_conditions,
                            generate_password_hash, find_all_instances)

from v1.config.database_conf import get_db

from sqlalchemy.ext.asyncio import AsyncSession

partners_router = APIRouter(prefix="/partners")


@partners_router.get("/public/{partner_id}", response_model=PublicPartner)
async def get_public_partner(partner_id: int,
                             db_session: AsyncSession = Depends(get_db)):
    partner = await find_instance(
        db_session,
        Partner,
        Partner.partner_id == partner_id,
        f"There is no record for requested partner ID value: {partner_id}",
    )
    return PublicPartner.from_attributes(partner)


@partners_router.get("/public/", response_model=List[PublicPartner])
async def get_public_partners(db_session: AsyncSession = Depends(get_db)):
    partners_all = await find_all_instances(
        db_session,
        Partner,
        f'{"Partners not found"}'
    )
    return [PublicPartner.from_attributes(partner) for partner in partners_all]


@partners_router.get("/private/{partner_id}", response_model=PrivatePartner)
async def get_private_partner(partner_id: int,
                              db_session: AsyncSession = Depends(get_db)):
    partner = await find_instance(
        db_session,
        Partner,
        Partner.partner_id == partner_id,
        f"There is no record for requested partner ID value: {partner_id}",
    )
    return PrivatePartner.from_attributes(partner)


@partners_router.get("/private/", response_model=List[PrivatePartner])
async def get_private_partners(db_session: AsyncSession = Depends(get_db)):
    partners_all = await find_all_instances(
        db_session,
        Partner,
        f'{"Partners not found"}'
    )
    private_partners = [PrivatePartner.from_attributes(
        partner) for partner in partners_all]
    return private_partners


@partners_router.post("/private/", response_model=PrivatePartner)
async def create_partner(partner: PrivatePartner,
                         db_session: AsyncSession = Depends(get_db)):
    async with db_session.begin():
        # Check if the region ID exists
        if not await exist(db_session, RegionsRussiaModel,
                           RegionsRussiaModel.id == partner.region_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid region_id. Region does not exist."
            )

        conditions = [
            Partner.inn == partner.inn,
            Partner.kpp == partner.kpp,
            Partner.ogrn == partner.ogrn,
            Partner.organization_email == partner.organization_email,
            Partner.organization_phone == partner.organization_phone,
        ]

        if await check_multiple_conditions(db_session, Partner, *conditions):
            raise HTTPException(
                status_code=400,
                detail="Partner with given details already exists")

        # Generate a UUID for the new partner
        new_partner_id = uuid4()

        # Create a new Partner instance
        new_partner = Partner(
            id=new_partner_id,
            organization_name=partner.organization_name,
            organization_website=partner.organization_website,
            organization_description=partner.organization_description,
            organization_email=partner.organization_email,
            organization_phone=partner.organization_phone,
            inn=partner.inn,
            kpp=partner.kpp,
            ogrn=partner.ogrn,
            hash_password=generate_password_hash(partner.hash_password),
            region_id=partner.region_id,
        )

        # Create a new PartnerAddress instance (if provided)
        # if partner.address:
        #     new_partner_address = PartnerAddress(
        #         partner_id=new_partner_id,
        #         street=partner.address.street,
        #         city=partner.address.city,
        #         postal_code=partner.address.postal_code,
        #     )
        #     db_session.add(new_partner_address)

        try:

            # Insert the new partner into the database
            db_session.add(new_partner)
            await db_session.flush()

            # Create a PrivatePartner instance
            # using the data from the created partner
            created_partner = PrivatePartner(**new_partner.__dict__)

            return created_partner

        except TypeError as te:

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(te))
