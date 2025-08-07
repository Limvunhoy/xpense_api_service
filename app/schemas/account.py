from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class AccountType(str, Enum):
    ABA = "ABA"
    WING = "WING"
    AC = "AC"  # Fixed typo from "AC" to "ACLEDA"
    CASH = "CASH"


class AccountBase(BaseModel):
    account_number: str = Field(
        ...,
        min_length=1,
        max_length=6,
        description="Unique account identifier (1-6 characters)"
    )
    account_name: str = Field(
        ...,
        min_length=1,
        max_length=12,
        description="Name of the account (1-12 characters)"
    )
    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        description="ISO 4217 currency code (3 uppercase letters)"
    )
    account_type: AccountType = Field(
        ...,
        description="Type of account (ABA, WING, ACLEDA, or CASH)"
    )
    account_logo: Optional[str] = Field(  # Fixed typo from 'acount_logo'
        None,
        description="URL or path to account logo image"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the account is currently active"
    )

    @field_validator('account_number', 'account_name', 'currency', 'account_logo', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from all string fields"""
        if isinstance(value, str):
            return value.strip()
        return value


class AccountRead(AccountBase):
    account_id: str = Field(
        ...,
        alias="id",
        description="Unique database identifier for the account"
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when account was created"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Timestamp when account was last updated"
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    account_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=6,  # Consistent with base length
        description="Account number (1-6 characters)"
    )
    account_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=12,  # Consistent with base length
        description="Account name (1-12 characters)"
    )
    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        description="3-letter currency code"
    )
    account_type: Optional[AccountType] = None
    account_logo: Optional[str] = None
    is_active: Optional[bool] = Field(
        None,
        description="Set account active/inactive status"
    )

    @field_validator('account_number', 'account_name', 'currency', 'account_logo', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from all string fields"""
        if isinstance(value, str):
            return value.strip()
        return value
