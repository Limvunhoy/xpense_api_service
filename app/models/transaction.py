from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone

from .account import Account
from .category import Category
from typing import Optional


class Transaction(SQLModel, table=True):
    # id: str | None = Field(default_factory=lambda: str(
    #     uuid.uuid4()), primary_key=True)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    currency: str
    amount: float

    note: str | None = None
    account_id: UUID = Field(foreign_key="account.account_id")
    category_id: UUID = Field(foreign_key="category.id")

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    transaction_date: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))

    account: Account | None = Relationship(back_populates="transactions")
    category: Category | None = Relationship(back_populates="transactions")
