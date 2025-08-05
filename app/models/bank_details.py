from pydantic import BaseModel

class BankDetails(BaseModel):
    bank_name: str
    bank_logo: str