from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class CategoryBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        examples=["Food & Dining"],
        description="Name of the category (1-100 characters)"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        examples=["All restaurant and food-related expenses"],
        description="Detailed description of the category (max 500 chars)"
    )
    icon_url: Optional[str] = Field(
        None,
        max_length=255,
        examples=["/static/icons/restaurant.svg"],
        description="URL path to the category icon (max 255 chars)"
    )

    @field_validator('name', 'description', 'icon_url', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace from string fields"""
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value


class CategoryRead(CategoryBase):
    id: UUID = Field(
        ...,
        examples=["123e4567-e89b-12d3-a456-426614174000"],
        description="Unique identifier for the category"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat(),  # For any future datetime fields
            UUID: lambda v: str(v)  # Ensure UUIDs are serialized as strings
        }
    )


class CategoryCreate(CategoryBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Transportation",
                "description": "All transport-related expenses",
                "icon_url": "/static/icons/car.svg"
            }
        }
    )


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        examples=["Updated Category Name"],
        description="Updated name of the category"
    )
    description: Optional[str] = Field(
        None,
        max_length=500,
        examples=["Updated category description"],
        description="Updated description of the category"
    )
    icon_url: Optional[str] = Field(
        None,
        max_length=255,
        examples=["/static/icons/updated-icon.svg"],
        description="Updated URL path to the category icon"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Updated Transportation",
                "description": "Updated transport expenses",
                "icon_url": "/static/icons/bus.svg"
            }
        }
    )

    @field_validator('name', 'description', 'icon_url', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip leading/trailing whitespace from string fields"""
        if value is None:
            return None
        return value.strip() if isinstance(value, str) else value
