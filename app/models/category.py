from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

from app.core.helper.timezones import get_now_utc_plus_7

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Category(SQLModel, table=True):
    # id: UUID = Field(default_factory=lambda: str(
    #     uuid.uuid4()), primary_key=True)
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    icon_url: str
    created_at: datetime = Field(default_factory=get_now_utc_plus_7)
    updated_at: Optional[datetime] = None

    transactions: List["Transaction"] = Relationship(back_populates="category")
