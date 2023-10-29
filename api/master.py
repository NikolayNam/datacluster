from fastapi import FastAPI
import uvicorn
from v1.main import datacluster_api_v1
from v1 import security

# app.mount("/api/v2", v2)

if __name__ == "__main__":
    uvicorn.run("master:datacluster_api_v1",
                host="0.0.0.0",
                port=8080,
                reload=True,
                ssl_keyfile=security.ssl_keyfile,
                ssl_certfile=security.ssl_certfile
                )
