from __future__ import annotations
from datetime import datetime, date, time
import pandas as pd
from email.message import EmailMessage
from uuid import uuid4
from fastapi import FastAPI, HTTPException, UploadFile, Depends
from starlette.responses import RedirectResponse
import asyncio
import aiosmtplib
from io import StringIO
from sqlalchemy import create_engine, MetaData, text
from sqlalchemy.orm import sessionmaker, Session

from pydantic import BaseModel, Field
from app import controller as Controller
from app.bootstrap import ApplicationBootstrap

bootstrap = ApplicationBootstrap()
bootstrap.create_tables()
app = FastAPI()


@app.get("/", tags=["Home"])
async def redirect():
    response = RedirectResponse(url='/docs')
    return response

app.include_router(
    Controller.router,
    prefix="/application",
    tags=["app controller"],
    # dependencies=[Depends(api_key)],
)
