from fastapi import FastAPI
from contextlib import asynccontextmanager
from scalar_fastapi import get_scalar_api_reference
from app.database.session import create_database_tables

## Routers ###
from app.api.router import master_router


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    create_database_tables()
    yield
    print("Server Stopped!")


app = FastAPI(lifespan=lifespan_handler)

app.include_router(master_router)


### API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
