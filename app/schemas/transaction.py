from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, field_validator, field_serializer
from typing import Optional
from datetime import datetime, timezone
from app.schemas.wallet import AccountRead
from app.schemas.category import CategoryRead

# --- Base model for UTC timestamps ---


class BaseUTCModel(BaseModel):
    """Base model to handle UTC datetime serialization"""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }
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

    transaction_date: datetime = Field(
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
    # transaction_id: str = Field(
    #     ...,
    #     description="Unique identifier for the transaction"
    # )
    transaction_no: str = Field(
        ...,
        description="Unique identifier for the transaction"
    )

    user_id: int

    wallet: AccountRead
    category: Optional[CategoryRead]

# --- Create Schema ---


class TransactionCreate(TransactionBase):
    wallet_id: str = Field(
        ...,
        description="Reference to associated wallet"
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

    wallet_id: Optional[str] = Field(
        None,
        description="Updated wallet reference"
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
