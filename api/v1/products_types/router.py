from fastapi import APIRouter, Depends
from fastapi import HTTPException
from v1.config.database_conf import get_db
from v1.products_types.models import ProductTypeSchema
from v1.products_types.models import ProductTypeTreeSchema
from v1.products_types.schemas import ProductType, ProductTypeTree, ProductTypeFrontend
from v1.utils.db_utils import find_instance, find_all_instances
from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

products_types_router = APIRouter(prefix="/api/products_types")


@products_types_router.get("/{product_type_id}", response_model=ProductType)
async def get_products_types(product_type_id: int,
                             db_session: AsyncSession = Depends(get_db)
                             ):
    products_type = await find_instance(
        db_session,
        ProductTypeSchema,
        ProductTypeSchema.product_type_id == product_type_id,
        f"There is no record for requested product_type_id ID value: {
            product_type_id}"
    )
    return ProductType.model_dump(products_type)


@products_types_router.get("/", response_model=List[ProductTypeFrontend])
async def get_products_types_all(db_session: AsyncSession = Depends(get_db)):
    ProductTypeJoin = join(ProductType, ProductTypeTree,
                           ProductType.product_type_id == ProductTypeTree.product_type_parent_id)
    products_types_all = select(ProductType.product_type_id, ProductType.product_type_name,
                                ProductTypeTree.product_type_parent_id,  ProductType.product_type).select_from(ProductTypeJoin)
    return [ProductTypeFrontend.model_dump(products_types) for products_types in products_types_all]


@products_types_router.get("/tree/{product_type_id}", response_model=ProductTypeTree)
async def get_products_types_tree(product_type_id: int,
                                  db_session: AsyncSession = Depends(get_db)
                                  ):
    stmt = select(ProductTypeSchema.product_type, ProductTypeSchema.product_type_id, ProductTypeTreeSchema.product_type_parent_id).join(
        ProductTypeSchema, ProductTypeSchema.product_type_id == ProductTypeTreeSchema.product_type_id).where(
        ProductTypeTreeSchema.product_type_id == product_type_id)
    result = await db_session.execute(stmt)
    instances = result.fetchone()

    if not instances:
        raise HTTPException(
            status_code=404,
            detail={"Records not found": "There is no record"},
        )
    else:
        return ProductTypeTree.model_dump(instances)


@products_types_router.get("/tree/", response_model=List[ProductTypeTree])
async def get_products_types_tree_name(db_session: AsyncSession = Depends(get_db)):
    stmt = select(ProductTypeSchema.product_type, ProductTypeSchema.product_type_id, ProductTypeTreeSchema.product_type_parent_id).join(
        ProductTypeSchema, ProductTypeSchema.product_type_id == ProductTypeTreeSchema.product_type_id)
    result = await db_session.execute(stmt)
    instances = result.fetchall()

    if not instances:
        raise HTTPException(
            status_code=404,
            detail={"Records not found": "There is no record"},
        )
    else:
        return [ProductTypeTree.model_dump(product_type_tree_all) for product_type_tree_all in instances]
