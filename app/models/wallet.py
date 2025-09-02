from uuid import uuid4
from sqlalchemy import Column, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlmodel import DateTime, SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from enum import Enum
from datetime import datetime
from typing import Optional

from app.core.helper.timezones import get_now_utc_plus_7
from app.models.user import User

if TYPE_CHECKING:
    from .transaction import Transaction


class Wallet(SQLModel, table=True):
    __tablename__ = "wallets"
    """
    Database model representing a expense wallet.
    """
    wallet_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        unique=True,
        max_length=36,
        nullable=False,
        description="Primary key stored as UUID string"
    )

    wallet_number: str = Field(
        index=True, nullable=False,
        unique=True,
        description="Wallet number"
    )

    wallet_name: str = Field(
        nullable=False,
        description="Wallet display name"
    )

    currency: str = Field(
        max_length=3, nullable=False,
        description="ISO 4217 currency code"
    )

    wallet_type: str = Field(
        nullable=False,
        description="Type of the wallet (e.g, ABA, WING, AC, CASH, ...)"
    )

    wallet_logo: Optional[str] = Field(
        default=None,
        description="URL or path to wallet logo image"
    )

    is_active: bool = Field(
        default=True, index=True,
        description="Flag to mark wallet as active/inactive"
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
            # PostgreSQL will auto-update it when the row is modified.
            onupdate=func.now(),
            nullable=False
        )
    )

    # Link to user
    user_id: int = Field(foreign_key="users.id")
    user: Optional[User] = Relationship(back_populates="wallets")

    # Relationships
    transactions: List["Transaction"] = Relationship(back_populates="wallet")

    def __repr__(self) -> str:
        return f"<Wallet {self.wallet_name} ({self.wallet_id})>"
