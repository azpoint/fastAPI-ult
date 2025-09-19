from typing import Any
from fastapi import FastAPI, status, HTTPException
from scalar_fastapi import get_scalar_api_reference


app = FastAPI()

db = {
    24345: {
        "weight": 0.2,
        "content": "paint",
        "status": "delivered",
    },
    24346: {
        "weight": 3.5,
        "content": "books",
        "status": "in transit",
    },
    24347: {
        "weight": 1.1,
        "content": "laptop",
        "status": "pending",
    },
    24348: {
        "weight": 2.8,
        "content": "clothes",
        "status": "shipped",
    },
    24349: {
        "weight": 0.7,
        "content": "toys",
        "status": "delivered",
    },
    24350: {
        "weight": 5.0,
        "content": "furniture",
        "status": "in transit",
    },
}


# Get the latest shipemnt
@app.get("/shipment/latest")
async def get_latest_shipment() -> dict[str, Any]:
    last_id = max(db.keys())
    return db[last_id]


### Get shipment by query parameter
@app.get("/shipment")
async def get_shipment_by_query(id: int | None = None) -> dict[str, Any]:

    if not id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="You need to provide an ID"
        )

    if id not in db:
        return {"detail": "Package does not exist"}

    return db[id]


# ### Get shipment by path parameter
# @app.get("/shipment/{id}")
# async def get_shipment_by_params(id: int) -> dict[str, Any]:

#     if id not in db:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Given ID does not exists"
#         )
#     return db[id]


# Create shipment
@app.post("/shipment")
async def submit_shipment(req_body: dict[str, Any]) -> dict[str, Any]:

    content = req_body["content"]
    weight = req_body["weight"]

    if weight > 25:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Shipment over the 25Kg limits",
        )

    new_id = max(db.keys()) + 1

    db[new_id] = {"content": content, "weight": weight, "status": "placed"}

    return {"id": new_id}


# @app.get("/shipment/{field}")
# async def get_shipment_field(field: str, id: int) -> dict[str, Any]:
#     return {field: db[id][field]}


# Update shipment
@app.put(("/shipment"))
async def shipment_update(
    id: int,
    content: str,
    weight: float,
    status: str,
) -> dict[str, Any]:

    db[id] = {"content": content, "weight": weight, "status": status}

    return db[id]


# Update shipment by field
@app.patch("/shipment")
async def patch_shipment(id: int, req_body: dict[str, Any]):
    shipment = db[id]
    # Update the provided fields

    shipment.update(req_body)

    db[id] = shipment

    return shipment


# Delete shipment by id
@app.delete("/shipment")
async def delete_shipment_by_id(id: int) -> dict[str, Any]:

    if id not in db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    shipment_deleted = db.pop(id)

    return {"detail": f"Shipment {id} deleted!", "deleted": shipment_deleted}


### API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title="Scalar API")
