from uuid import uuid4
from fastapi import APIRouter, UploadFile, Depends, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
# from app.database import get_db
from app.repository import Repository
from app.service import Service
from datetime import datetime
import pandas as pd
import asyncio
from io import StringIO
from sqlalchemy.orm import sessionmaker, Session
from loguru import logger


router = APIRouter()

@cbv(router)
class Controller:
    def __init__(self):
        self.service = Service()

    @router.get("/hello_world")
    def hello_world(self):
        from app.db import db_billet, db_documents_received, db_email_sent_history
        breakpoint()
        return {"message": "Hello World"}

    @router.post("/send_email_to_list")
    async def send_email_to_list(self, document: UploadFile, background_tasks: BackgroundTasks):
        try:
            # process_uuid = uuid4().hex
            # contents = document.file.read()
            # contents = contents.decode('utf-8')
            # file_name = document.filename
            # background_tasks.add_task(
            #     self.service.execute,
            #     contents=contents,
            #     process_uuid=process_uuid,
            #     file_name=file_name
            # )
            logger.info('iniciando tudo')
            total_time = await self.service.execute(document=document)
            return total_time
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
