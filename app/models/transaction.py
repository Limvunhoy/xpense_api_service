from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone, timedelta

from app.core.helper.timezones import get_now_utc_plus_7

from .account import Account
from .category import Category
from typing import Optional


class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    currency: str
    amount: float
    note: str | None = None
    account_id: UUID = Field(foreign_key="account.account_id")
    category_id: UUID = Field(foreign_key="category.id")

    created_at: datetime = Field(default_factory=get_now_utc_plus_7)
    updated_at: Optional[datetime] = Field(default=None, nullable=True)
    transaction_date: datetime = Field(default_factory=get_now_utc_plus_7)

    account: Account | None = Relationship(back_populates="transactions")
    category: Category | None = Relationship(back_populates="transactions")
