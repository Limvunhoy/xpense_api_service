from pydantic import BaseModel, Field, field_validator
from typing import Optional


class AccountBase(BaseModel):
    account_number: str = Field(..., min_length=1, max_length=50)
    account_name: str = Field(..., min_length=1, max_length=100)
    currency: str = Field(..., min_length=3, max_length=3,
                          pattern="^[A-Z]{3}$")

    @field_validator('account_number', 'account_name', 'currency', mode='before')
    def strip_whitespace(cls, value: str) -> str:
        return value.strip() if isinstance(value, str) else value


class AccountRead(AccountBase):
    account_id: str = Field(..., alias="id")

    class Config:
        from_attributes = True
        populate_by_name = True  # Allows both alias and original field name


class AccountCreate(AccountBase):
    pass


class AccountUpdate(BaseModel):
    account_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=50,
        description="Account number (optional for update)"
    )
    account_name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Account name (optional for update)"
    )
    currency: Optional[str] = Field(
        None,
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        description="3-letter currency code (optional for update)"
    )

    @field_validator('account_number', 'account_name', 'currency', mode='before')
    def strip_whitespace(cls, value: Optional[str]) -> Optional[str]:
        return value.strip() if isinstance(value, str) else value
