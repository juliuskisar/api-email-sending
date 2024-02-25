from datetime import datetime
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()



class DocumentsReceivedEntity(Base):
    __tablename__ = 'documents_received'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_name = Column(String, nullable=False)
    number_of_rows = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class EmailSentHistoryEntity(BaseModel): # table name "email_sent_history"
    hsitory_id: int # chave primária, auto increment
    email: str # chave estrangeira
    name: str
    billet_id: int
    created_at: datetime = datetime.now()
    deleted_at: datetime = None


class BilletEntity(BaseModel): # table name "billet"
    billet_id: str # chave primária
    email: int # chave estrangeira
    ammount: float = Field(..., alias="debtAmount")
    due_date: str = Field(..., alias="dueDate")
    code_bar: str = Field(..., alias="billetUrl")
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    canceled_at: datetime = None


