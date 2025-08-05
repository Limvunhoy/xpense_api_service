from pydantic import BaseModel
from datetime import datetime


class CategoryBase(BaseModel):
    name: str
    description: str | None = None


class CategoryRead(CategoryBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    name: str | None = None
    description: str | None = None
