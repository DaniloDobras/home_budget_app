from datetime import datetime

from pydantic import BaseModel, Field


class BillRequest(BaseModel):
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    category_id: int


class BillResponse(BillRequest):
    id: int
    user_id: int
