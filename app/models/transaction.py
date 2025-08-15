from uuid import uuid4
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
from enum import Enum

from app.core.helper.timezones import get_now_utc_plus_7

if TYPE_CHECKING:
    from .account import Account
    from .category import Category


class TransactionBase(SQLModel):
    """Base model containing common transaction fields."""
    amount: float = Field(
        nullable=False,
        gt=0,
        description="Positive monetary value of the transaction"
    )

    currency: str = Field(
        max_length=3,
        nullable=False,
        description="ISO 4217 currency code (e.g., USD, KHR)"
    )

    note: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Additional context or memo about the transaction"
    )

    transaction_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
        description="Effective date/time of the transaction"
    )

    is_active: bool = Field(
        default=True,
        index=True,
        description="Soft delete flag for transaction"
    )


class Transaction(TransactionBase, table=True):
    """Database model representing a financial transaction."""
    # transaction_id: UUID = Field(
    #     default_factory=uuid4,
    #     # primary_key=True,
    #     # index=True,
    #     # sa_column_kwargs={"unique": True},
    #     sa_column=Column(
    #         PG_UUID(as_uuid=True),
    #         primary_key=True,
    #         unique=True, nullable=False
    #     )
    # )
    transaction_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        unique=True,
        max_length=36,
        nullable=False,
        description="Primary key stored as UUID string"
    )

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )

    updated_at: Optional[datetime] = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now(),
            onupdate=func.now(),
            nullable=False
        )
    )

    # Foreign keys
    account_id: str = Field(
        foreign_key="account.account_id",
        nullable=False,
        description="Reference to associated account"
    )

    category_id: Optional[str] = Field(
        foreign_key="category.category_id",
        default=None,
        description="Optional reference to category"
    )

    # Relationships
    account: "Account" = Relationship(back_populates="transactions")

    category: Optional["Category"] = Relationship(
        back_populates="transactions")

    def __repr__(self) -> str:
        return f"<Transaction {self.amount} {self.currency} ({self.transaction_id})>"

    def __str__(self) -> str:
        return f"Transaction of {self.amount} {self.currency} on {self.transaction_date.isoformat()}"
