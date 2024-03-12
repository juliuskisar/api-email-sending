from __future__ import annotations
from loguru import logger
from fastapi import FastAPI
from starlette.responses import RedirectResponse


from app import controller as Controller
from app.database import create_tables, engine, metadata, database

logger.add("app/logs/file_app.log", rotation="10 MB")

metadata.create_all(engine)
create_tables()
app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", tags=["Home"])
async def redirect():
    response = RedirectResponse(url='/docs')
    return response

app.include_router(
    Controller.router,
    prefix="/application",
    tags=["app controller"],
)
