from typing import Any
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference
from app.schemas import ShipmentCreate, ShipmentRead, ShipmentUpdate

app = FastAPI()

shipments = {
    24345: {
        "weight": 0.2,
        "content": "paint",
        "status": "delivered",
        "destination": "New York",
    },
    24346: {
        "weight": 3.5,
        "content": "books",
        "status": "in_transit",
        "destination": "Los Angeles",
    },
    24347: {
        "weight": 1.1,
        "content": "laptop",
        "status": "placed",
        "destination": "Chicago",
    },
    24348: {
        "weight": 2.8,
        "content": "clothes",
        "status": "placed",
        "destination": "Houston",
    },
    24349: {
        "weight": 0.7,
        "content": "toys",
        "status": "delivered",
        "destination": "Miami",
    },
    24350: {
        "weight": 5.0,
        "content": "furniture",
        "status": "in_transit",
        "destination": "Seattle",
    },
}


# Get the latest shipment
@app.get("/shipment/latest")
async def get_latest_shipment() -> dict[str, Any]:
    last_id = max(shipments.keys())

    return {"id": last_id, **shipments[last_id]}


### Get shipment by ID
@app.get("/shipment", response_model=ShipmentRead)
async def get_shipment_by_id(id: int):

    if not id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="You need to provide an ID"
        )

    return shipments[id]


# Create shipment
@app.post("/shipment")  # , response_model=ShipmentRead)
async def submit_shipment(req_body: ShipmentCreate):

    new_id = max(shipments.keys()) + 1

    shipments[new_id] = {
        "content": req_body.content,
        "weight": req_body.weight,
        "status": "placed",
        "destination": req_body.destination,
    }

    return {"id": new_id, **shipments[new_id]}


# Update shipment by field
@app.patch("/shipment", response_model=ShipmentRead)
async def update_shipment(id: int, body: ShipmentUpdate):

    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Shipment ID does not exist"
        )

    shipments[id].update(body)

    return shipments[id]


# Delete shipment by id
@app.delete("/shipment")
async def delete_shipment_by_id(id: int) -> dict[str, Any]:

    if id not in shipments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    shipment_deleted = shipments.pop(id)

    return {"detail": f"Shipment {id} deleted!", "deleted": shipment_deleted}


### API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
