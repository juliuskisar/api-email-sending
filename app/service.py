from fastapi import UploadFile
from app.models import BilletState, DocumentsReceivedState, EmailSentHistoryInterface
from loguru import logger
from datetime import date, datetime
from uuid import uuid4
from io import StringIO
import pandas as pd
from app.repository import Repository
from app.db import db_billet, db_documents_received


class Service:
    def __init__(self):
        self.repository = Repository()

    async def execute(
        self,
        filename: str,
        contents: str,
        process_uuid: str
    ):
        logger.info(f'starting process for document {filename}')
        start_time = datetime.now()
        df = pd.read_csv(StringIO(contents))
        logger.info(f'Dez primeiros itens do documento {filename} - {df.head(10)}')
        db_documents_received.append(
            DocumentsReceivedState(
                process_uuid=process_uuid,
                document_name=filename,
                number_of_items=len(df)
            )
        )
        for row in df.itertuples(index=False):
            self._create_billet_and_send_email(
                row.email, row.name, row.debtAmount, row.debtDueDate
            )
        end_time = datetime.now()
        total_time = end_time - start_time
        db_documents_received[-1].process_finished = True
        db_documents_received[-1].process_finished_at = datetime.now()
        logger.info(f" document status - {db_documents_received[-1]}")
        logger.info(f"total time {total_time} - process_uuid: {process_uuid} - document_name: {filename} - number_of_rows: {len(df)}")
        return total_time

    def get_process_status(self, process_uuid: str):
        status = next(item for item in db_documents_received if item.process_uuid == process_uuid)
        if not status:
            return {"message": "process not found"}
        return status

    def get_email_sent_history(self, email: str):
        billets_sent = [item for item in db_billet if item.email == email]
        return EmailSentHistoryInterface.build(billets_sent)

    def get_process_history(self):
        return db_documents_received

    def _create_billet_and_send_email(
            self,
            email: str,
            name: str,
            amount: float,
            due_date: date,
            count=1
        ):
        billet_uuid = self._create_billet(email=email, name=name, amount=amount, due_date=due_date)
        try:
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


    def _create_billet(self, email: str, name: str, amount: float, due_date: str):
        # função que cria boleto
        billet_uuid = uuid4().hex
        db_billet.append(
            BilletState(
                uuid=billet_uuid,
                name=name,
                email=email,
                amount=amount,
                due_date=due_date,
                code_bar="1234567890"
            )
        )

        return billet_uuid

    def _send_email(self, email: str, name: str, billet_uuid: int):
        # função que envia email com boleto
        pass

