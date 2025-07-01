from pydantic import BaseModel


class CategoryRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str
