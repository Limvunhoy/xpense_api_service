# from datetime import datetime
# from pydantic import BaseModel
# from app.schemas.account import AccountRead
# from app.schemas.category import CategoryRead


# class TransactionRead(BaseModel):
#     id: str
#     currency: str
#     amount: float
#     note: str | None = None
#     account: AccountRead
#     category: CategoryRead
#     created_at: datetime

#     class Config:
#         from_attributes = True
