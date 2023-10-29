from fastapi.openapi.utils import get_openapi
import redis

from fastapi import FastAPI

# my package modules
from v1.auth.router import auth_router
from v1.addresses.router import address_router
from v1.partners.router import partners_router
from v1.regions.router import regions_router
from v1.users.router import users_router
from v1.tables_type.router import tables_type_router
from v1.products_types.router import products_types_router
from v1.streaming.router import streaming_router
import v1.security

datacluster_api_v1 = FastAPI(title="DataCluster")

r = redis.Redis(
    host='redis-12727.c14.us-east-1-2.ec2.cloud.redislabs.com',
    port=12727,
    password='5V4JOsHc9ap4Po1bxfCJGPQVXhj8EskM')

v1.security.setup_security(datacluster_api_v1)

# for exec docker container
# docker compose up --build -d


def custom_openapi():
    if datacluster_api_v1.openapi_schema:
        return datacluster_api_v1.openapi_schema
    openapi_schema = get_openapi(
        title="DataCluster API",
        version="1.1.0",
        description="API created for DataCluster",
        routes=datacluster_api_v1.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    datacluster_api_v1.openapi_schema = openapi_schema
    return datacluster_api_v1.openapi_schema


datacluster_api_v1.openapi = custom_openapi

# users
datacluster_api_v1.include_router(auth_router, tags=["auth users router"])


# partners
datacluster_api_v1.include_router(partners_router, tags=["partners router"])

# partners_address
datacluster_api_v1.include_router(address_router,
                                  tags=["partners address router"])

# partners_address
datacluster_api_v1.include_router(streaming_router,
                                  tags=["streaming router"])

# regions
datacluster_api_v1.include_router(regions_router, tags=["regions router"])

# users
datacluster_api_v1.include_router(users_router, tags=["users router"])

# types
datacluster_api_v1.include_router(
    tables_type_router, tags=["tables type router"])

# products_types
datacluster_api_v1.include_router(
    products_types_router, tags=["products types router"])
