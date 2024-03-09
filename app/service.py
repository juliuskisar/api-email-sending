from concurrent.futures import ProcessPoolExecutor
import multiprocessing
from time import sleep
from fastapi import UploadFile
from app.models import Billet, BilletState, DocumentsReceivedState, EmailSentHistoryState
from loguru import logger
from datetime import date, datetime
from uuid import uuid4
# from app.models import BilletEntity
from io import StringIO
import pandas as pd
import asyncio
from app.repository import Repository
from app.db import db_billet, db_documents_received, db_email_sent_history
# from app.database import get_db


class Service:
    def __init__(self):
        self.repository = Repository()

    async def execute(self, document: UploadFile):
        logger.info(f'starting process for document {document.filename}')
        start_time = datetime.now()
        contents = document.file.read()
        contents = contents.decode('utf-8')
        # document.file.seek(0)
        df = pd.read_csv(StringIO(contents))
        df_top_10 = df
        
        # rows = [(row.email, row.name, row.debtAmount, row.debtDueDate) for row in df_top_10.itertuples(index=False)]

        # num_workers = multiprocessing.cpu_count()
        # with ProcessPoolExecutor(max_workers=num_workers) as executor:
        #     logger.info('passou por aqui')
        # # Ajuste para passar os dados serializáveis
        #     from app.service import Service
        #     service = Service()
        #     results = list(executor.map(service.process_multi_thread, *zip(*rows)))

        for row in df_top_10.itertuples(index=False):
            self._create_billet_and_send_email(
                row.email, row.name, row.debtAmount, row.debtDueDate)
        # tasks = [
        # self._create_billet_and_send_email(
        #     row.email, row.name, row.debtAmount, row.debtDueDate)
        #     for row in df_top_10.itertuples(index=False)
        # ]
        # await asyncio.gather(*tasks)
        process_uuid = uuid4().hex
        db_documents_received[process_uuid] = DocumentsReceivedState(
            process_uuid=process_uuid,
            document_name=document.filename,
            number_of_items=len(df_top_10)
        )
        # await self.repository.save_document_received(df=df, file_name=document.filename, process_uuid=process_uuid)
        end_time = datetime.now()
        total_time = end_time - start_time
        # email_history_example = await self.repository.get_emails_sent_history()
        logger.info(f"total time {total_time} - process_uuid: {process_uuid} - document_name: {document.filename} - number_of_rows: {len(df_top_10)}")
        return total_time

    def _create_billet_and_send_email(
            self,
            email: str,
            name: str,
            amount: float,
            due_date: date,
            count=1
        ):
        try:
            billet_uuid = self._create_billet(email=email, amount=amount, due_date=due_date)
            self._send_email(email=email, name=name, billet_uuid=billet_uuid)
        except Exception as e:
            logger.info(f"Error sending email to {email} in attempt {count}: {e}")
            if count < 4:
                self._create_billet_and_send_email(
                    email=email,
                    name=name,
                    amount=amount,
                    due_date=due_date,
                    count=count+1
                )
            else:
                logger.info(f"Failed to send email to {email} after 3 attempts")


    def _create_billet(self, email: str, amount: float, due_date: str):
        # função que cria boleto
        billet_uuid = uuid4().hex
        db_billet[email] = BilletState(
            uuid=billet_uuid,
            email=email,
            amount=amount,
            due_date=due_date,
            code_bar="1234567890"
        )

        return billet_uuid
        # return await self.repository.save_billet(
        #     email=email,
        #     amount=amount,
        #     due_date=due_date,
        #     code_bar="1234567890"
        # )

    def _send_email(self, email: str, name: str, billet_uuid: int):
        # função que envia email com boleto
        db_email_sent_history[email] = EmailSentHistoryState(
            uuid=uuid4().hex,
            email=email,
            name=name,
            billet_uuid=billet_uuid
        )
        # await self.repository.save_email_sent_history(email=email, name=name, billet_id=billet_id)
