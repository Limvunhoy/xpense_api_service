import uuid
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime, timezone

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class Category(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(
        uuid.uuid4()), primary_key=True)
    name: str = Field(index=True)
    description: Optional[str] = None
    created_at: datetime = Field(default=datetime.now(timezone.utc))

    transactions: List["Transaction"] = Relationship(back_populates="category")
