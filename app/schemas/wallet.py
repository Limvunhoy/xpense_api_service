from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from enum import Enum
# from uuid import UUID

from app.core.helper.timezones import get_now_utc_plus_7


class AccountType(str, Enum):
    """
    Enum representing supported wallet types with enhanced metadata.
    """
    ABA = "ABA"
    WING = "WING"
    AC = "AC"
    CASH = "CASH"
    CREDIT = "CREDIT"
    INVESTMENT = "INVESTMENT"

    @classmethod
    def get_description(cls) -> str:
        """Returns formatted description of all wallet types."""
        descriptions = {
            cls.ABA: "ABA Bank Wallet",
            cls.WING: "Wing Bank Wallet",
            cls.AC: "ACLEDA Bank Wallet",
            cls.CASH: "Physical Cash Holdings",
            cls.CREDIT: "Credit Card Wallet",
            cls.INVESTMENT: "Investment Portfolio",
        }
        return " | ".join([f"{item.value} ({descriptions[item]})" for item in cls])


class AccountBase(BaseModel):
    """
    Shared fields and validation for Wallet schemas.
    """
    wallet_number: str = Field(
        ...,
        min_length=1,
        max_length=12,
        pattern=r"^[A-Z0-9\-]+$",
        examples=["123456789", "ACC-123-XYZ"],
        description="Unique wallet identifier/number (alphanumeric and hyphens)",
    )

    wallet_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s\-&]+$",
        examples=["ABA Primary Wallet", "Cash Wallet"],
        description="Display name for the wallet (2-50 alphanumeric characters)",
    )

    currency: str = Field(
        ...,
        min_length=3,
        max_length=3,
        examples=["USD", "KHR"],
        description="ISO 4217 currency code",
    )

    wallet_type: AccountType = Field(
        ...,
        examples=["ABA"],
        description=f"Type of wallet. Options: {AccountType.get_description()}",
    )

    wallet_logo: Optional[str] = Field(
        None,
        max_length=255,
        # pattern=r"^\/static\/logos\/[a-zA-Z0-9\-_]+\.(png|jpg|svg)$",
        examples=["/static/logos/aba.png"],
        description="URL path to wallet logo (PNG/JPG/SVG, max 255 chars)",
    )

    # is_active: bool = Field(
    #     True,
    #     examples=[True],
    #     description="Active status of the wallet (default: True)",
    # )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "wallet_number": "123-456-789",
                "wallet_name": "Main ABA Wallet",
                "currency": "USD",
                "wallet_type": "ABA",
                "wallet_logo": "/static/logos/aba.png",
                # "is_active": True,
            }
        }
    )

    @field_validator("wallet_number", "wallet_name", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty or whitespace only")
        return value

    @field_validator("wallet_type", mode="before")
    def validate_wallet_type(cls, value):
        if value not in AccountType.__members__ and value not in [at.value for at in AccountType]:
            raise ValueError(
                f"Invalid wallet type '{value}'. "
                f"Must be one of: {', '.join([at.value for at in AccountType])}"
            )
        return value


class AccountRead(AccountBase):
    """
    Schema for reading wallet data with additional metadata.
    """
    wallet_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="Unique system-generated wallet identifier",
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
    Schema for creating a new wallet.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "wallet_number": "WING-987-654",
                "wallet_name": "Wing Savings Wallet",
                "currency": "KHR",
                "wallet_type": "WING",
                "wallet_logo": "/static/logos/wing.png",
            }
        }
    )


class AccountUpdate(BaseModel):
    """
    Schema for updating an existing wallet with partial updates.
    """
    wallet_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=20,
        pattern=r"^[A-Z0-9\-]+$",
        examples=["UPD-123-456"],
        description="Updated wallet number",
    )

    wallet_name: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        pattern=r"^[a-zA-Z0-9\s\-&]+$",
        examples=["Updated Wallet Name"],
        description="Updated wallet name",
    )

    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        examples=["KHR"],
        description="Updated currency code",
    )

    wallet_type: Optional[AccountType] = Field(
        None,
        examples=["AC"],
        description="Updated wallet type",
    )

    wallet_logo: Optional[str] = Field(
        None,
        max_length=255,
        # pattern=r"^\/static\/logos\/[a-zA-Z0-9\-_]+\.(png|jpg|svg)$",
        examples=["/static/logos/aba.png"],
        description="URL path to wallet logo (PNG/JPG/SVG, max 255 chars)",
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
                "wallet_name": "Updated Wallet Name",
                # "is_active": True,
            }
        }
    )

    @field_validator("wallet_number", "wallet_name", mode="before")
    def _strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        """Remove whitespace and validate string fields."""
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field cannot be empty or whitespace only")
        return value


class AccountDelete(BaseModel):
    wallet_id: str = Field(
        ...,
        examples=["550e8400-e29b-41d4-a716-446655440000"],
        description="Unique system-generated wallet identifier",
    )
