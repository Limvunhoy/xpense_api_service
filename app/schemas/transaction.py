from pydantic import BaseModel
from app.schemas.account import AccountRead
from app.schemas.category import CategoryRead


class TransactionBase(BaseModel):
    currency: str
    amount: float
    note: str | None = None

    class Config:
        from_attributes = True


class TransactionRead(TransactionBase):
    id: str
    account: AccountRead
    category: CategoryRead


class TransactionCreate(TransactionBase):
    account_id: str
    category_id: str


class TransactionUpdate(TransactionBase):
    currency: str | None = None
    amount: float | None = None
    note: str | None = None
    account: AccountRead | None = None
    category: CategoryRead | None = None
