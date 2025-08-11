from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon_url: Optional[str] = Field(
        None,
        max_length=255,
        description="Full URL of the icon, e.g. '/static/icons/restaurant.svg'"
    )

    @field_validator('name', 'description', 'icon_url', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value


class CategoryRead(CategoryBase):
    id: UUID
    # No computed fields needed because icon_url is stored directly

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    icon_url: Optional[str] = Field(None, max_length=255)

    @field_validator('name', 'description', 'icon_url', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value
