from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from sqlalchemy import Column, func
from sqlmodel import DateTime, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .account import Account
    from .category import Category
    from .transaction import Transaction


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True),
            server_default=func.now()
        )
    )

    token_version: int = Field(default=0, nullable=False)
    accounts: List["Account"] = Relationship(back_populates="user")
    categories: List["Category"] = Relationship(back_populates="user")
    transactions: List["Transaction"] = Relationship(back_populates="user")
