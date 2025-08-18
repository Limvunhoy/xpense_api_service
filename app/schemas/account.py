from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from enum import Enum
# from uuid import UUID

from app.core.helper.timezones import get_now_utc_plus_7


class AccountType(str, Enum):
    """
    Enum representing supported account types with enhanced metadata.
    """
    ABA = "ABA"
    WING = "WING"
    AC = "AC"
    CASH = "CASH"
    CREDIT = "CREDIT"
    INVESTMENT = "INVESTMENT"

    @classmethod
    def get_description(cls) -> str:
        """Returns formatted description of all account types."""
        descriptions = {
            cls.ABA: "ABA Bank Account",
            cls.WING: "Wing Bank Account",
            cls.AC: "ACLEDA Bank Account",
            cls.CASH: "Physical Cash Holdings",
            cls.CREDIT: "Credit Card Account",
            cls.INVESTMENT: "Investment Portfolio",
        }
        return " | ".join([f"{item.value} ({descriptions[item]})" for item in cls])


class AccountBase(BaseModel):
    """
    Shared fields and validation for Account schemas.
    """
    account_number: str = Field(
        ...,
        min_length=1,
        max_length=12,
        pattern=r"^[A-Z0-9\-]+$",
        examples=["123456789", "ACC-123-XYZ"],
        description="Unique account identifier/number (alphanumeric and hyphens)",
    )

    account_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s\-&]+$",
        examples=["ABA Primary Account", "Cash Wallet"],
        description="Display name for the account (2-50 alphanumeric characters)",
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        examples=["USD", "KHR"],
        description="ISO 4217 currency code",
    )

    account_type: AccountType = Field(
        ...,
        examples=["ABA"],
        description=f"Type of account. Options: {AccountType.get_description()}",
    )

    account_logo: Optional[str] = Field(
        None,
        max_length=255,
        # pattern=r"^\/static\/logos\/[a-zA-Z0-9\-_]+\.(png|jpg|svg)$",
        examples=["/static/logos/aba.png"],
        description="URL path to account logo (PNG/JPG/SVG, max 255 chars)",
    )

    # is_active: bool = Field(
    #     True,
    #     examples=[True],
    #     description="Active status of the account (default: True)",
    # )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_number": "123-456-789",
                "account_name": "Main ABA Account",
                "currency": "USD",
                "account_type": "ABA",
                "account_logo": "/static/logos/aba.png",
                # "is_active": True,
            }
        }
    )

    @field_validator("account_number", "account_name", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty or whitespace only")
        return value


class AccountRead(AccountBase):
    """
    Schema for reading account data with additional metadata.
    """
    account_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="Unique system-generated account identifier",
    )

    user_id: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
        },
    )


class AccountCreate(AccountBase):
    """
    Schema for creating a new account.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_number": "WING-987-654",
                "account_name": "Wing Savings Account",
                "currency": "KHR",
                "account_type": "WING",
                "account_logo": "/static/logos/wing.png",
            }
        }
    )


class AccountUpdate(BaseModel):
    """
    Schema for updating an existing account with partial updates.
    """
    account_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        pattern=r"^[A-Z0-9\-]+$",
        examples=["UPD-123-456"],
        description="Updated account number",
    )

    account_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s\-&]+$",
        examples=["Updated Account Name"],
        description="Updated account name",
    )

    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        examples=["KHR"],
        description="Updated currency code",
    )

    account_type: Optional[AccountType] = Field(
        None,
        examples=["AC"],
        description="Updated account type",
    )

    # is_active: Optional[bool] = Field(
    #     None,
    #     examples=[False],
    #     description="Updated active status",
    # )

    # updated_at: Optional[datetime] = Field(
    #     default_factory=get_now_utc_plus_7,
    # )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_name": "Updated Account Name",
                # "is_active": True,
            }
        }
    )

    @field_validator("account_number", "account_name", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty or whitespace only")
        return value


class AccountDelete(BaseModel):
    account_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="Unique system-generated account identifier",
    )
