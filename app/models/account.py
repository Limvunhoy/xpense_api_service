from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from enum import Enum
from datetime import datetime
from typing import Optional

from app.core.helper.timezones import get_now_utc_plus_7

if TYPE_CHECKING:
    from .transaction import Transaction


class Account(SQLModel, table=True):
    """
    Database model representing a expense account.
    """
    account_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True, index=True
    )

    account_number: str = Field(
        index=True, nullable=False,
        unique=True,
        description="Account number"
    )

    account_name: str = Field(
        nullable=False,
        description="Account display name"
    )

    currency: str = Field(
        max_length=3, nullable=False,
        description="ISO 4217 currency code"
    )

    account_type: str = Field(
        nullable=False,
        description="Type of the account (e.g, ABA, WING, AC, CASH, ...)"
    )

    account_logo: Optional[str] = Field(
        default=None,
        description="URL or path to account logo image"
    )

    is_active: bool = Field(
        default=True, index=True,
        description="Flag to mark account as active/inactive"
    )

    created_at: datetime = Field(default_factory=get_now_utc_plus_7)

    updated_at: Optional[datetime] = Field(
        default_factory=get_now_utc_plus_7,
        nullable=True
    )

    # Relationships
    transactions: List["Transaction"] = Relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"<Account {self.account_name} ({self.account_id})>"
