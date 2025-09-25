from contextlib import asynccontextmanager
from fastapi import FastAPI
from rich import print, panel


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel("ServerStarted...", border_style="green"))
    yield
    print(panel.Panel("Server Stopped!", border_style="red"))


app = FastAPI(lifespan=lifespan_handler)


@app.get("/")
async def read_rrot():
    return {"detail": "Server running..."}
