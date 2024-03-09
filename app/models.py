from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BilletState(BaseModel):
    uuid: str
    email: str
    amount: str
    due_date: str
    code_bar: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    canceled_at: datetime = None


class EmailSentHistoryState(BaseModel):
    uuid: str
    email: str
    name: str
    billet_uuid: str
    created_at: datetime = datetime.now()
    deleted_at: datetime = None


class DocumentsReceivedState(BaseModel):
    process_uuid: str
    document_name: str
    number_of_items: int
    created_at: datetime = datetime.now()

class DocumentsReceived(Base):
    __tablename__ = 'documents_received'
    
    id = Column(Integer, primary_key=True, index=True)
    process_uuid = Column(String, nullable=False)
    document_name = Column(String, nullable=False)
    number_of_rows = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    @classmethod
    def from_dict(cls, document_dict):
        return cls(
            document_name=document_dict['document_name'],
            number_of_rows=document_dict['number_of_rows']
        )
    
    @classmethod
    def to_dict(cls):
        return {
            'id': cls.id,
            'document_name': cls.document_name,
            'number_of_rows': cls.number_of_rows,
            'created_at': cls.created_at
        }

class EmailSentHistory(Base):
    __tablename__ = 'email_sent_history'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    billet_id = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    deleted_at = Column(DateTime)

    @classmethod
    def from_dict(cls, email_sent_history_dict):
        return cls(
            email=email_sent_history_dict['email'],
            name=email_sent_history_dict['name'],
            billet_id=email_sent_history_dict['billet_id']
        )
    
    @classmethod
    def to_dict(cls):
        return {
            'id': cls.id,
            'email': cls.email,
            'name': cls.name,
            'billet_id': cls.billet_id,
            'created_at': cls.created_at,
            'deleted_at': cls.deleted_at
        }

class Billet(Base):
    __tablename__ = 'billet'
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    amount = Column(String, nullable=False)
    due_date = Column(String, nullable=False)
    code_bar = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    canceled_at = Column(DateTime)

    @classmethod
    def from_dict(cls, billet_dict):
        return cls(
            id=billet_dict['billet_id'],
            email=billet_dict['email'],
            amount=billet_dict['amount'],
            due_date=billet_dict['due_date'],
            code_bar=billet_dict['code_bar']
        )
    
    @classmethod
    def to_dict(cls):
        return {
            'id': cls.id,
            'billet_id': cls.id,
            'email': cls.email,
            'amount': cls.amount,
            'due_date': cls.due_date,
            'code_bar': cls.code_bar,
            'created_at': cls.created_at,
            'updated_at': cls.updated_at,
            'canceled_at': cls.canceled_at
        }


# from datetime import datetime
# from pydantic import BaseModel, Field
# from sqlalchemy import Table, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from app.database import metadata

# Base = declarative_base()

# documents_received = Table(
#     'documents_received',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('document_name', String, nullable=False),
#     Column('number_of_rows', Integer, nullable=False),
#     Column('created_at', DateTime, default=datetime.now)
# )

# email_sent_history = Table(
#     'email_sent_history',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('email', String, nullable=False),
#     Column('name', String, nullable=False),
#     Column('billet_id', String, nullable=False),
#     Column('created_at', DateTime, default=datetime.now),
#     Column('deleted_at', DateTime, nullable=True)
# )

# billet = Table(
#     'billet',
#     metadata,
#     Column('id', Integer, primary_key=True, autoincrement=True),
#     Column('billet_id', String, nullable=False),
#     Column('email', String, nullable=False),
#     Column('ammount', String, nullable=False),
#     Column('due_date', String, nullable=False),
#     Column('code_bar', String, nullable=False),
#     Column('created_at', DateTime, default=datetime.now),
#     Column('updated_at', DateTime, default=datetime.now),
#     Column('canceled_at', DateTime, nullable=True)
# )
