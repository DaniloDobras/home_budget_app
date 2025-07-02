from datetime import datetime

from pydantic import BaseModel, Field

from app.api.schema.category_schema import CategoryResponse


class BillRequest(BaseModel):
    description: str
    amount: float
    date: datetime = Field(default_factory=datetime.utcnow)
    category_id: int


class BillResponse(BaseModel):
    id: int
    user_id: int
    category: CategoryResponse


class TopUpRequest(BaseModel):
    amount: float = Field(..., gt=0,
                          description="Amount to top up (must be > 0)")


class TopUpResponse(BaseModel):
    message: str
    new_balance: float
