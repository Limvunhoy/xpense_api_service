from pydantic import BaseModel


class AccountBase(BaseModel):
    account_number: str
    account_name: str
    # payment_type: str
    currency: str


class AccountRead(AccountBase):
    account_id: str

    class Config:
        from_attributes = True


class AccountCreate(AccountBase):
    pass


class AccountUpdate(AccountBase):
    account_number: str | None = None
    payment_type: str | None = None
    currency: str | None = None
