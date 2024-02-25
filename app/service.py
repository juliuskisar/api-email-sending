from fastapi import UploadFile

from datetime import date, datetime
from uuid import uuid4
from app.models import BilletEntity
from io import StringIO
import pandas as pd
import asyncio
from app.repository import Repository
from app.database import get_db


class Service:
    def __init__(self):
        self.repository = Repository(db=get_db())

    async def execute(self, document: UploadFile):
        start_time = datetime.now()
        contents = document.file.read()
        contents = contents.decode('utf-8')
        # document.file.seek(0)
        df = pd.read_csv(StringIO(contents))
        tasks = [
        self._create_billet_and_send_email(
            row.email, row.name, row.debtAmount, row.debtDueDate)
            for row in df.itertuples(index=False)
        ]
        await asyncio.gather(*tasks)
        await self.repository.save_document_received(df=df, document=document)
        end_time = datetime.now()
        total_time = end_time - start_time
        documents_received = await self.repository.get_documents_received()
        breakpoint()
        return documents_received, total_time

    async def _create_billet_and_send_email(self, email: str, name: str, ammount: float, due_date: date):
        # message = EmailMessage()
        # message["From"] = "juliuskisar.test@gmail.com"
        # message["To"] = email_address
        # message["Subject"] = "Assunto do E-mail"
        # message.set_content("Corpo do E-mail")
        
        # await aiosmtplib.send(message, hostname="smtp.gmail.com", port=587, username="juliuskisar.teste@gmail.com", password="pmch efjp beva ipqj", start_tls=True)
        # trecho não será executado para evitar bloqueio
        billet_id = uuid4().hex
        billet = await self._create_billet(email=email, ammount=ammount, due_date=due_date, billet_id=billet_id)
        email_sent = await self._send_email(email=email, name=name, billet=billet)
        await self.repository.save_email_sent_history(email=email, name=name, billet_id=billet_id)
        pass

    async def register_documents_received(document):
        pass

    async def _create_billet(self, email: str, ammount: float, due_date: str, billet_id: str):
        # Criar boleto e salvar no banco de dados
        await self.repository.save_billet(email=email, billet_id=billet_id, ammount=ammount, due_date=due_date, code_bar="1234567890")
        pass

    async def _send_email(self, email: str, name: str, billet):
        # Enviar e-mail com boleto
        pass

