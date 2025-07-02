from datetime import datetime

from pydantic import BaseModel, Field

from app.api.schema.category_schema import CategoryResponse


class BillRequest(BaseModel):
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    category_id: int
    top_up: bool = Field(default=False)


class UpdateBillRequest(BaseModel):
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    category_id: int


class BillResponse(BaseModel):
    id: int
    user_id: int
    description: str
    amount: float
    category: CategoryResponse
