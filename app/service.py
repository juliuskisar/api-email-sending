from fastapi import UploadFile

from datetime import date, datetime
from uuid import uuid4
# from app.models import BilletEntity
from io import StringIO
import pandas as pd
import asyncio
from app.repository import Repository
# from app.database import get_db


class Service:
    def __init__(self):
        self.repository = Repository()

    async def execute(self, document: UploadFile):
        start_time = datetime.now()
        contents = document.file.read()
        contents = contents.decode('utf-8')
        # document.file.seek(0)
        df = pd.read_csv(StringIO(contents))
        df_top_10 = df.head(1)
        semaphore = asyncio.Semaphore(100)
        tasks = [
        self._create_billet_and_send_email_limited(
            semaphore, row.email, row.name, row.debtAmount, row.debtDueDate)
            for row in df_top_10.itertuples(index=False)
        ]
        await asyncio.gather(*tasks)
        await self.repository.save_document_received(df=df, document=document)
        end_time = datetime.now()
        total_time = end_time - start_time
        email_history_example = await self.repository.get_email_history(billet_id=1)
        return email_history_example, total_time

    async def _create_billet_and_send_email_limited(
        self,
        semaphore,
        email: str,
        name: str,
        amount: float,
        due_date: date
    ):
        async with semaphore:
            await self._create_billet_and_send_email(
                email=email,
                name=name,
                amount=amount,
                due_date=due_date
            )

    async def _create_billet_and_send_email(self, email: str, name: str, amount: float, due_date: date):
        try:
            billet_id = uuid4().hex
            billet_id = await self._create_billet(email=email, amount=amount, due_date=due_date, billet_id=billet_id)
            await self._send_email(email=email, name=name, billet_id=billet_id)
        except Exception as e:
            print(f"Error sending email to {email}: {e}")

    async def _create_billet(self, email: str, amount: float, due_date: str, billet_id: str):
        # função que cria boleto
        return await self.repository.save_billet(
            email=email,
            billet_id=billet_id,
            amount=amount,
            due_date=due_date,
            code_bar="1234567890"
        )

    async def _send_email(self, email: str, name: str, billet_id: int):
        # função que envia email com boleto
        await self.repository.save_email_sent_history(email=email, name=name, billet_id=billet_id)

