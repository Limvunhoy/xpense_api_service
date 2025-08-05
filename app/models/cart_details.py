from pydantic import BaseModel

class CartDetails(BaseModel):
    cart_type: str
    linked_service: str
    last_four_digits: str