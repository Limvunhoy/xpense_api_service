import pytest
from datetime import datetime
from .transaction import Transaction

def test_transaction(): 
    transaction = Transaction(
        id="TXN001",
        currency="USD",
        amount=100,
        created_at=datetime.now(),
        note="Food & Drink"
    )

    assert transaction.id == "TXN001"
    assert transaction.currency == "USD"
    assert transaction.amount == 100
    assert isinstance(transaction.created_at, datetime)
    assert transaction.note == "Food & Drink"