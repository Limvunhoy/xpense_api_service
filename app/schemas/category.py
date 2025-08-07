from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(...,
                      min_length=1,
                      max_length=100,
                      description="Name of the category (1-100 characters)")

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional description of the category (max 500 characters)"
    )

    @field_validator('name', 'description', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value


class CategoryRead(CategoryBase):
    id: str = Field(..., description="Unique identifier for the category")
    created_at: datetime = Field(...,
                                 description="Timestamp when category was created")

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()  # Ensure proper datetime serialization
        }


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="New name for the category (optional)"
    )

    description: Optional[str] = Field(
        None,
        max_length=500,
        description="New description for the category (optional)"
    )

    @field_validator('name', 'description', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        """Strip whitespace from string fields"""
        return value.strip() if isinstance(value, str) else value
