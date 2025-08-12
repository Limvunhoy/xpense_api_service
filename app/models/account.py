from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship

from app.core.helper.timezones import get_now_utc_plus_7

from .cart_details import CartDetails
from .bank_details import BankDetails
from datetime import datetime
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Account(SQLModel, table=True):
    # account_id: str = Field(default_factory=lambda: str(
    #     uuid.uuid4()), primary_key=True)
    account_id: UUID = Field(default_factory=uuid4, primary_key=True)
    account_number: str
    account_name: str
    account_type: str
    account_logo: str
    currency: str
    is_active: bool
    created_at: datetime = Field(
        default_factory=get_now_utc_plus_7)
    updated_at: Optional[datetime] = Field(default=None)

    transactions: list["Transaction"] = Relationship(back_populates="account")
