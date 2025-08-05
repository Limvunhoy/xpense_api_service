import uuid
from sqlmodel import SQLModel, Field, Relationship
from .cart_details import CartDetails
from .bank_details import BankDetails
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Account(SQLModel, table=True):
    account_id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    account_number: str
    account_name: str
    # payment_type: str
    currency: str
    # cart_details: CartDetails
    # bank_details: BankDetails
    created_at: datetime = Field(default_factory=datetime.now)

    transactions: list["Transaction"] = Relationship(back_populates="account")
