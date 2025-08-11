from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, field_validator
from typing import Optional
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead
from uuid import UUID
from datetime import datetime


class TransactionBase(BaseModel):
    amount: PositiveFloat
    note: Optional[str] = None
    transaction_date: datetime = Field(
        ...,
        description="Date when the transaction occurred")

    class Config:
        from_attributes = True

    @field_validator('note', mode='before')
    def strip_whitespace(cls, value):
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value


class TransactionRead(TransactionBase):
    id: UUID
    currency: str = Field(..., min_length=3, max_length=3,
                          pattern="^[A-Z]{3}$")
    account: AccountRead
    category: CategoryRead
    # created_at: datetime
    # updated_at: Optional[datetime] = Field(
    #     None,
    #     description="Timestamp when transaction was last updated."
    # )

    # class Config:
    #     from_attributes: True
    #     json_encoders = {datetime: lambda v: v.isoformat()}
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,  # Required for alias to work
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        },
    )


class TransactionCreate(TransactionBase):
    account_id: UUID
    category_id: UUID
    currency: str = Field(
        ..., min_length=3, max_length=3,
        pattern="^[A-Z]{3}$"
    )


class TransactionUpdate(BaseModel):
    amount: Optional[PositiveFloat] = None
    note: Optional[str] = None
    description: Optional[str] = Field(None, min_length=1)
    account_id: Optional[UUID] = None
    category_id: Optional[UUID] = None
    currency: Optional[str] = Field(
        None, min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when transaction was last updated."
    )

    @field_validator('currency', 'note', 'description', mode='before')
    def strip_whitespace(cls, value):
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value
