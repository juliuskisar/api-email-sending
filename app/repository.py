from sqlalchemy.orm import Session
from app.models import Billet, DocumentsReceived, EmailSentHistory
from datetime import date, datetime
from app.database import database

class Repository:

    async def save_document_received(self, df, file_name: str, process_uuid: str):
        document_dict = {
            'process_uuid': process_uuid,
            'document_name': file_name,
            'number_of_rows': len(df),
            'created_at': datetime.now()
        }
        query = DocumentsReceived.__table__.insert().values(document_dict)
        last_record_id = await database.execute(query)
        return last_record_id

    async def get_documents_received(self):
        query = DocumentsReceived.__table__.select()
        return await database.fetch_all(query)

    async def get_billet(self, billet_id):
        query = Billet.__table__.select().where(Billet.id == billet_id)
        return await database.fetch_one(query)
    
    async def get_email_history(self, billet_id):
        query = EmailSentHistory.__table__.select().where(EmailSentHistory.billet_id == billet_id)
        return await database.fetch_one(query)

    async def get_emails_sent_history(self):
        query = EmailSentHistory.__table__.select()
        return await database.fetch_all(query)

    async def save_email_sent_history(self, email: str, name: str, billet_id: str):
        email_history_dict = {
            'email': email,
            'name': name,
            'billet_id': billet_id,
            'created_at': datetime.now()
        }
        query = EmailSentHistory.__table__.insert().values(email_history_dict)
        last_record_id = await database.execute(query)
        return last_record_id

    async def save_billet(self, email: str, amount: float, due_date: date, code_bar: str):
        billet_dict = {
            'email': email,
            'amount': amount,
            'due_date': due_date,
            'code_bar': code_bar,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        query = Billet.__table__.insert().values(billet_dict)
        last_record_id = await database.execute(query)
        return last_record_id

