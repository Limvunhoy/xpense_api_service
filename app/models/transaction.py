import uuid
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime

from .account import Account
from .category import Category


class Transaction(SQLModel, table=True):
    id: str | None = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    currency: str
    amount: float
    # created_at: datetime = Field(default_factory=lambda: datetime.now(datetime.timezone.utc))
    note: str | None = None
    account_id: str = Field(foreign_key="account.account_id")
    category_id: str = Field(foreign_key="category.id")

    account: Account | None = Relationship(back_populates="transactions")
    category: Category | None = Relationship(back_populates="transactions")


# class TransactionUpdate(SQLModel):
#     currency: str | None = None
#     amount: float | None = None
#     note: str | None = None
#     account_id: str | None = None
#     category_id: str | None = None
