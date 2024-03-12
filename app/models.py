from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BilletState(BaseModel):
    uuid: str
    name: str
    email: str
    amount: str
    due_date: str
    code_bar: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    canceled_at: datetime = None


class EmailSentHistoryInterface(BaseModel):
    email: str
    name: str
    billet_uuid: str
    sent_in: datetime

    @classmethod
    def build(cls, billet_list: list):
        return [
            cls(
                email=item.email,
                name=item.name,
                billet_uuid=item.uuid,
                sent_in=item.created_at
            ) for item in billet_list
        ]


class DocumentsReceivedState(BaseModel):
    process_uuid: str
    document_name: str
    number_of_items: int
    process_finished: bool = False
    created_at: datetime = datetime.now()
    process_finished_at: datetime = None
