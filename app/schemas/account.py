from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from enum import Enum
from uuid import UUID


class AccountType(str, Enum):
    ABA = "ABA"
    WING = "WING"
    ACELEDA = "AC"  # Changed from "AC" to be more descriptive
    CASH = "CASH"

    @classmethod
    def get_description(cls) -> str:
        return " | ".join([f"{item.value} ({item.name})" for item in cls])


class AccountBase(BaseModel):
    account_number: str = Field(
        ...,
        min_length=1,
        max_length=20,  # Increased from 9 to accommodate various bank formats
        examples=["123456789", "ACC123"],
        description="Unique account identifier/number"
    )
    account_name: str = Field(
        ...,
        min_length=1,
        max_length=50,  # Increased from 12 for better usability
        examples=["ABA Primary", "Cash Wallet"],
        description="Display name for the account"
    )
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        examples=["USD", "KHR"],
        description="ISO 4217 currency code (e.g. USD, KHR)"
    )
    account_type: AccountType = Field(
        ...,
        examples=["ABA"],
        description=f"Type of account. Options: {AccountType.get_description()}"
    )
    account_logo: Optional[str] = Field(
        None,
        examples=["/static/logos/aba.png"],
        description="URL or path to account logo image (optional)"
    )
    is_active: bool = Field(
        default=True,
        examples=[True],
        description="Active status of the account (default: True)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_number": "123456789",
                "account_name": "Main Account",
                "currency": "USD",
                "account_type": "ABA",
                "account_logo": "/static/logos/aba.png",
                "is_active": True
            }
        }
    )

    @field_validator('account_number', 'account_name', 'currency', 'account_logo', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Automatically strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value


class AccountRead(AccountBase):
    account_id: UUID = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="System-generated unique identifier"
    )
    created_at: datetime = Field(
        ...,
        examples=["2023-01-01T00:00:00+07:00"],
        description="Timestamp of account creation (UTC+7)"
    )
    updated_at: Optional[datetime] = Field(
        None,
        examples=["2023-01-02T00:00:00+07:00"],
        description="Timestamp of last update (UTC+7)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
    )


class AccountCreate(AccountBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_number": "987654321",
                "account_name": "New Account",
                "currency": "KHR",
                "account_type": "WING",
                "account_logo": "/static/logos/wing.png",
                "is_active": True
            }
        }
    )


class AccountUpdate(BaseModel):
    account_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        examples=["654321987"],
        description="Updated account number"
    )
    account_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        examples=["Updated Account"],
        description="Updated account name"
    )
    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        examples=["KHR"],
        description="Updated currency code"
    )
    account_type: Optional[AccountType] = Field(
        None,
        examples=["CASH"],
        description="Updated account type"
    )
    account_logo: Optional[str] = Field(
        None,
        examples=["/static/logos/updated.png"],
        description="Updated logo path"
    )
    is_active: Optional[bool] = Field(
        None,
        examples=[False],
        description="Updated active status"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_name": "Updated Name",
                "currency": "USD",
                "is_active": False
            }
        }
    )

    @field_validator('account_number', 'account_name', 'currency', 'account_logo', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Automatically strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value
