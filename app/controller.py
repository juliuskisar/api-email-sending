from uuid import uuid4
from fastapi import APIRouter, UploadFile, BackgroundTasks
from fastapi.exceptions import HTTPException
from fastapi_utils.cbv import cbv
from app.service import Service
import pandas as pd
from loguru import logger


router = APIRouter()

@cbv(router)
class Controller:
    def __init__(self):
        self.service = Service()

    @router.get("/hello_world")
    def hello_world(self):
        from app.db import db_billet, db_documents_received, db_email_sent_history
        return {"message": "Hello World"}

    @router.post("/send_email_to_list")
    async def send_email_to_list(self, document: UploadFile, background_tasks: BackgroundTasks):
        try:
            process_uuid = uuid4().hex
            contents = document.file.read()
            contents = contents.decode('utf-8')
            filename = document.filename
            background_tasks.add_task(
                self.service.execute,
                contents=contents,
                process_uuid=process_uuid,
                filename=filename
            )
            return {
                "message: ": "process started", 
                "process_uuid": process_uuid
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

    @router.get("/get_process_status/{process_uuid}")
    def get_process_status(self, process_uuid: str):
        try:
            return self.service.get_process_status(process_uuid)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)

    @router.get("/get_email_sent_history")
    def get_email_sent_history(self, email: str):
        
        try:
            return self.service.get_email_sent_history(email=email)
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
    
    @router.get("/get_process_history")
    def get_process_history(self):
        try:
            return self.service.get_process_history()
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)