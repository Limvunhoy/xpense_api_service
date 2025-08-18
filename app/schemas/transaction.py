from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, field_validator, field_serializer
from typing import Optional
from datetime import datetime, timezone
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead

# --- Base model for UTC timestamps ---


class BaseUTCModel(BaseModel):
    """Base model to handle UTC datetime serialization"""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.isoformat()}
    )

# --- Transaction Base ---


class TransactionBase(BaseUTCModel):
    amount: PositiveFloat = Field(
        ...,
        gt=0,
        description="Positive monetary value of the transaction"
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        description="ISO 4217 currency code"
    )

    note: Optional[str] = Field(
        None,
        max_length=500,
        description="Additional context or memo about the transaction"
    )

    transaction_date: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Transaction datetime in UTC"
    )

    @field_validator("note", mode="before")
    def strip_note(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Note cannot be empty or whitespace only")
        return value

# --- Read Schema ---


class TransactionRead(TransactionBase):
    transaction_id: str = Field(
        ...,
        description="Unique identifier for the transaction"
    )

    user_id: int

    account: AccountRead
    category: Optional[CategoryRead]

# --- Create Schema ---


class TransactionCreate(TransactionBase):
    account_id: str = Field(
        ...,
        description="Reference to associated account"
    )

    category_id: Optional[str] = Field(
        None,
        description="Optional reference to category"
    )

# --- Update Schema ---


class TransactionUpdate(BaseModel):
    amount: Optional[PositiveFloat] = Field(
        None, gt=0,
        description="Updated transaction amount"
    )

    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        description="Updated currency code"
    )

    note: Optional[str] = Field(
        None,
        max_length=500,
        description="Updated transaction note"
    )

    account_id: Optional[str] = Field(
        None,
        description="Updated account reference"
    )

    category_id: Optional[str] = Field(
        None,
        description="Updated category reference"
    )

    @field_validator("note", mode="before")
    def strip_note(cls, value: Optional[str]) -> Optional[str]:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Note cannot be empty or whitespace only")
        return value

# --- Delete Schema ---


class TransactionDelete(BaseModel):
    transaction_id: str = Field(
        ...,
        description="Unique identifier for the transaction"
    )
