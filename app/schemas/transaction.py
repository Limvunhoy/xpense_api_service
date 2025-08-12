from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, field_serializer, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime
from app.core.helper.timezones import UTC_PLUS_7, get_now_utc_plus_7
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    amount: PositiveFloat = Field(
        ...,
        gt=0,
        examples=[100.50],
        description="Transaction amount (must be positive)"
    )
    note: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Dinner with clients"],
        description="Additional notes about the transaction"
    )
    transaction_date: datetime = Field(
        default_factory=get_now_utc_plus_7,
        # examples=["2023-12-01T14:30:00+07:00"],
        description="Transaction date in UTC+7 (Phnom Penh timezone)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda v: v.astimezone(
            UTC_PLUS_7).isoformat()}
    )

    # @field_serializer('transaction_date')
    # def serialize_dt(self, dt: datetime, _info) -> str:
    #     """Ensure datetime is always serialized with UTC+7 timezone"""
    #     return dt.astimezone(UTC_PLUS_7).isoformat()

    @field_validator('note', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value


class TransactionRead(TransactionBase):
    id: UUID = Field(..., examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"])
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        examples=["USD"],
        description="ISO 4217 currency code in uppercase"
    )
    account: AccountRead
    category: CategoryRead

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

    @field_serializer('transaction_date')
    def serialize_dt(self, dt: datetime, _info) -> str:
        """Serialize datetime for API output in UTC+7 ISO format"""
        return dt.astimezone(UTC_PLUS_7).isoformat()


class TransactionCreate(TransactionBase):
    account_id: UUID = Field(..., examples=[
                             "a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"])
    category_id: UUID = Field(..., examples=[
                              "b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9"])
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        examples=["USD"],
        description="ISO 4217 currency code in uppercase"
    )


class TransactionUpdate(BaseModel):
    amount: Optional[PositiveFloat] = Field(
        None,
        gt=0,
        examples=[150.75],
        description="Updated transaction amount (must be positive)"
    )
    note: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Updated dinner notes"],
        description="Updated transaction notes"
    )
    account_id: Optional[UUID] = Field(
        None,
        examples=["a1b2c3d4-e5f6-7890-g1h2-i3j4k5l6m7n8"],
        description="Updated account reference"
    )
    category_id: Optional[UUID] = Field(
        None,
        examples=["b2c3d4e5-f6g7-8901-h2i3-j4k5l6m7n8o9"],
        description="Updated category reference"
    )
    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        examples=["KHR"],
        description="Updated ISO 4217 currency code in uppercase"
    )
    updated_at: datetime = Field(
        default_factory=get_now_utc_plus_7,
        examples=["2023-12-01T15:45:00+07:00"],
        description="Automatic timestamp of last update in UTC+7"
    )

    model_config = ConfigDict(
        json_encoders={datetime: lambda v: v.astimezone(
            UTC_PLUS_7).isoformat()}
    )

    @field_validator('currency', 'note', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value
