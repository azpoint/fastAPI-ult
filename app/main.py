from typing import Any
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.database import Database

app = FastAPI()

db = Database()

# # Get the latest shipment
# @app.get("/shipment/latest")
# async def get_latest_shipment() -> dict[str, Any]:
#     last_id = max(shipments.keys())

#     return {"id": last_id, **shipments[last_id]}


### Get shipment by ID
@app.get("/shipment", response_model=ShipmentRead)
async def get_shipment_by_id(id: int):

    shipment = db.get(id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Given id doesn't exist!"
        )

    return shipment


# Create shipment
@app.post("/shipment", response_model=None)
async def submit_shipment(req_body: ShipmentCreate):

    new_id = db.create(req_body)

    return {"id": new_id}


# Update shipment by field
@app.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, req_body: ShipmentUpdate):

    shipment = db.update(id, req_body)

    return shipment


# Delete shipment by id
@app.delete("/shipment")
async def delete_shipment_by_id(id: int) -> dict[str, Any]:

    db.delete(id)

    return {"detail": f"Shipment {id} deleted!"}


### API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
