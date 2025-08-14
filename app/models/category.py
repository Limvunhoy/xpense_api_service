# Category Model
from uuid import uuid4
from sqlalchemy import Column, DateTime, func
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
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
    # category_id: UUID = Field(
    #     default_factory=uuid4,
    #     # primary_key=True,
    #     # index=True,
    #     # sa_column_kwargs={"unique": True}, # can remove this property because `unique=True` is already in the `sa_column`
    #     sa_column=Column(
    #         PG_UUID(as_uuid=True),
    #         primary_key=True,
    #         unique=True,
    #         nullable=False,
    #     ),
    #     description="Unique identifier for the category"
    # )

    category_id: str = Field(
        default_factory=lambda: str(uuid4()),
        primary_key=True,
        index=True,
        unique=True,
        max_length=36,
        nullable=False,
        description="Primary key stored as UUID string"
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
            onupdate=func.now(),
            nullable=False
        )
    )

    # Bidirectional relationship with transactions
    transactions: List["Transaction"] = Relationship(back_populates="category")

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.category_id})>"
