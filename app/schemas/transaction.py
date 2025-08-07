from pydantic import BaseModel, Field, PositiveFloat, field_validator
from typing import Optional
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    currency: str = Field(..., min_length=1)
    amount: PositiveFloat
    note: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator('currency', 'note', mode='before')
    def strip_whitespace(cls, value):
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value


class TransactionRead(TransactionBase):
    id: str
    account: AccountRead
    category: CategoryRead


class TransactionCreate(TransactionBase):
    account_id: str
    category_id: str


class TransactionUpdate(BaseModel):
    currency: Optional[str] = Field(None, min_length=1)
    amount: Optional[PositiveFloat] = None
    note: Optional[str] = None
    description: Optional[str] = Field(None, min_length=1)
    account_id: Optional[str] = None
    category_id: Optional[str] = None

    @field_validator('currency', 'note', 'description', mode='before')
    def strip_whitespace(cls, value):
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value
