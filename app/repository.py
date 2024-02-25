from datetime import date
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.models import BilletEntity, EmailSentHistoryEntity, DocumentsReceivedEntity
from pandas.core.frame import DataFrame



class Repository:
    def __init__(self, db: Session):
        self.db = db

    async def save_document_received(self, df, document):
        register = DocumentsReceivedEntity(
            document_name=document.filename,
            number_of_rows=len(df)
        )
        self.db.add(register)
        self.db.commit()

    async def get_documents_received(self):
        return self.db.query(DocumentsReceivedEntity).all()


    async def save_email_sent_history(self, email: str, name: str, billet_id: str):
        # Salvar no banco de dados
        pass

    async def save_billet(self, email: str, billet_id: str, ammount: float, due_date: date, code_bar: str):
        # Salvar no banco de dados
        pass
