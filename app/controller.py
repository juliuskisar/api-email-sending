from fastapi import APIRouter, UploadFile, Depends
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
from app.repository import Repository
from app.service import Service
from datetime import datetime
import pandas as pd
import asyncio
from io import StringIO
from sqlalchemy.orm import sessionmaker, Session


router = APIRouter()

@cbv(router)
class Controller:
    def __init__(self):
        self.service = Service()

    @router.get("/hello_world")
    def hello_world(self):
        return {"message": "Hello World"}

    @router.post("/send_email_to_list")
    async def send_email_to_list(self, document: UploadFile):
        try:
            response = await self.service.execute(document=document)
            return response
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
