# Category Model
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime

from app.core.helper.timezones import get_now_utc_plus_7

if TYPE_CHECKING:
    from .transaction import Transaction


class CategoryBase(SQLModel):
    """Base model for Category containing common fields."""
    name: str = Field(
        index=True,
        nullable=False,
        max_length=100,
        description="Category name"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Category description"
    )

    icon_url: Optional[str] = Field(
        default=None,
        max_length=255,
        description="URL to icon image"
    )

    is_active: bool = Field(
        default=True,
        index=True,
        description="Flag to mark category as active/inactive"
    )


class Category(CategoryBase, table=True):
    """Database model for Category."""
    category_id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        description="Unique identifier for the category"
    )

    created_at: datetime = Field(
        default_factory=get_now_utc_plus_7,
        nullable=False,
        description="Timestamp when category was created"
    )

    updated_at: Optional[datetime] = Field(
        default_factory=get_now_utc_plus_7, nullable=True)

    # Bidirectional relationship with transactions
    transactions: List["Transaction"] = Relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.category_id})>"
