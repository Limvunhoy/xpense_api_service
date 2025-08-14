from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, field_validator, field_serializer
from typing import Optional
from datetime import datetime
from enum import Enum

from app.core.helper.timezones import UTC_PLUS_7, get_now_utc_plus_7
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    """
    Shared fields and validation for Transaction schemas.
    """
    amount: PositiveFloat = Field(
        ...,
        gt=0,
        examples=[100.50],
        description="Positive monetary value of the transaction",
        json_schema_extra={"format": "decimal"},
    )

    note: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Dinner with clients"],
        description="Additional context or memo about the transaction",
    )

    transaction_date: datetime = Field(
        default_factory=get_now_utc_plus_7,
        description="Effective date/time in UTC+7 (Phnom Penh timezone)",
    )

    # is_active: bool = Field(
    #     True,
    #     examples=[True],
    #     description="Soft delete flag for transaction",
    # )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.astimezone(
            UTC_PLUS_7).isoformat()},
    )

    @field_validator("note", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Note cannot be empty or whitespace only")
        return value


class TransactionRead(TransactionBase):
    """
    Schema for reading transaction data with complete details.
    """
    transaction_id: str = Field(
        ...,
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
        description="Unique identifier for the transaction",
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        examples=["USD"],
        description="ISO 4217 currency code",
    )

    created_at: datetime = Field(
        ...,
        examples=["2023-01-01T00:00:00+07:00"],
        description="Timestamp when transaction was recorded",
    )

    updated_at: Optional[datetime] = Field(
        ...,
        examples=["2023-01-01T00:00:00+07:00"],
        description="Timestamp when transaction was last modified",
    )

    account: AccountRead = Field(
        ...,
        description="Associated account details",
    )

    category: Optional[CategoryRead] = Field(
        None,
        description="Associated category details (optional)",
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    @field_serializer("transaction_date", "created_at", "updated_at")
    def _serialize_datetime(self, dt: datetime, _info) -> str:
        """Serialize datetime for API output in UTC+7 ISO format."""
        return dt.astimezone(UTC_PLUS_7).isoformat()


class TransactionCreate(TransactionBase):
    """
    Schema for creating a new transaction with required references.
    """
    account_id: str = Field(
        ...,
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
        description="Reference to associated account",
    )

    category_id: Optional[str] = Field(
        None,
        examples=["b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9"],
        description="Optional reference to category",
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        examples=["USD"],
        description="ISO 4217 currency code",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "amount": 100.50,
                "note": "Dinner with clients",
                "account_id": "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8",
                "category_id": "b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9",
                "currency": "USD",
                # "is_active": True,
            }
        }
    )


class TransactionUpdate(BaseModel):
    """
    Schema for updating an existing transaction with partial updates.
    """
    amount: Optional[PositiveFloat] = Field(
        None,
        gt=0,
        examples=[150.75],
        description="Updated transaction amount (must be positive)",
    )

    note: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Updated dinner notes"],
        description="Updated transaction notes",
    )

    account_id: Optional[str] = Field(
        None,
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
        description="Updated account reference",
    )

    category_id: Optional[str] = Field(
        None,
        examples=["b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9"],
        description="Updated category reference",
    )

    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        examples=["KHR"],
        description="Updated currency code",
    )

    # is_active: Optional[bool] = Field(
    #     None,
    #     examples=[False],
    #     description="Update active status",
    # )

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.astimezone(
            UTC_PLUS_7).isoformat()},
        json_schema_extra={
            "example": {
                "amount": 150.75,
                "note": "Updated dinner notes",
                "currency": "KHR",
                # "is_active": False,
            }
        },
    )

    @field_validator("note", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Note cannot be empty or whitespace only")
        return value


class TransactionDelete(BaseModel):
    """
    Schema for deleting an existing transaction.
    """
    transaction_id: str = Field(
        ...,
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
        description="Unique identifier for the transaction",
    )
