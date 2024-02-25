from pydantic import BaseModel, Field


class Payload(BaseModel):
    name: str
    email: str
    government_id: str = Field(..., alias="governmentId")
    debt_amount: float = Field(..., alias="debtAmount")
    debt_duo_date: str = Field(..., alias="debtDueDate")
    debt_id: str = Field(..., alias="debtId")
