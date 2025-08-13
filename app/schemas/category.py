from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

from app.core.helper.timezones import get_now_utc_plus_7


class CategoryBase(BaseModel):
    """
    Shared fields and validation rules for Category schemas.
    """
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Food & Dining"],
        description="Name of the category (1-100 characters)",
        json_schema_extra={"pattern": r"^[a-zA-Z0-9\s&'-]+$"},
    )

    description: Optional[str] = Field(
        None,
        max_length=500,
        examples=["All restaurant and food-related expenses"],
        description="Detailed description of the category (max 500 chars)",
    )

    icon_url: Optional[str] = Field(
        None,
        max_length=255,
        examples=["/static/icons/restaurant.svg"],
        description="URL path to the category icon (max 255 chars)",
        pattern=r"^\/static\/icons\/[a-zA-Z0-9_-]+\.(svg|png|jpg)$",
    )

    # is_active: bool = Field(
    #     True,
    #     examples=[True],
    #     description="Active status of the category (default: True)",
    # )

    @field_validator("name", "description", "icon_url", mode="before")
    def _strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Remove leading/trailing whitespace from string fields."""
        return value.strip() if isinstance(value, str) else value


class CategoryRead(CategoryBase):
    """
    Schema for reading category data.
    """
    category_id: UUID = Field(
        ...,
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        description="Unique identifier for the category",
    )

    created_at: datetime = Field(
        ...,
        examples=["2023-01-01T00:00:00Z"],
        description="Timestamp when category was created",
    )

    updated_at: datetime = Field(
        ...,
        examples=["2023-01-01T00:00:00Z"],
        description="Timestamp when category was last updated",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        },
    )


class CategoryCreate(CategoryBase):
    """
    Schema for creating a new category.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Transportation",
                "description": "All transport-related expenses",
                "icon_url": "/static/icons/car.svg",
                # "is_active": True,
            }
        }
    )


class CategoryUpdate(BaseModel):
    """
    Schema for updating an existing category.
    """
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        examples=["Updated Category Name"],
        description="Updated name of the category",
        json_schema_extra={"pattern": r"^[a-zA-Z0-9\s&'-]+$"},
    )

    description: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Updated category description"],
        description="Updated description of the category",
    )

    icon_url: Optional[str] = Field(
        None,
        max_length=255,
        examples=["/static/icons/bus.svg"],
        description="Updated URL path to the category icon",
        pattern=r"^\/static\/icons\/[a-zA-Z0-9_-]+\.(svg|png|jpg)$",
    )

    # is_active: Optional[bool] = Field(
    #     None,
    #     examples=[False],
    #     description="Update active status",
    # )

    updated_at: Optional[datetime] = Field(
        default_factory=get_now_utc_plus_7,
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Transportation",
                "description": "Updated transport expenses",
                "icon_url": "/static/icons/bus.svg",
                # "is_active": False,
            }
        }
    )

    @field_validator("name", "description", "icon_url", mode="before")
    def _strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Remove leading/trailing whitespace from string fields."""
        return value.strip() if isinstance(value, str) else value


class CategoryDelete(BaseModel):
    """
    Schema for deleting an existing category.
    """
    category_id: UUID = Field(
        ...,
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        description="Unique identifier for the category",
    )
