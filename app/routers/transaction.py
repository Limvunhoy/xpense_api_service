from fastapi import APIRouter, Depends, status
from typing import List
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionRead, TransactionCreate, TransactionUpdate
from app.schemas.response import BaseResponse
from app.exceptions import AppHTTPException

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("/{id}", response_model=BaseResponse[TransactionRead])
def get_transaction(id: str, session: Session = Depends(get_session)):
    """
    Retrieve a single transaction by ID.
    """
    transaction = session.get(Transaction, id)
    if not transaction:
        raise AppHTTPException(
            result_code=404,
            result_message="Transaction not found",
            error_code="E404"
        )

    return BaseResponse(
        result_code=200,
        result_message="Success",
        data=transaction
    )


@router.post("/", response_model=BaseResponse[TransactionRead], status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction: TransactionCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new transaction.
    """
    new_transaction = Transaction(**transaction.model_dump())
    session.add(new_transaction)
    session.commit()
    session.refresh(new_transaction)

    return BaseResponse(
        result_code=201,
        result_message="Transaction created successfully",
        data=new_transaction
    )


@router.patch("/{id}", response_model=BaseResponse[TransactionRead])
async def update_transaction(
    id: str,
    transaction: TransactionUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing transaction by ID.
    """
    transaction_db = session.get(Transaction, id)
    if not transaction_db:
        raise AppHTTPException(
            result_code=404,
            result_message="Transaction not found",
            error_code="E404"
        )

    transaction_data = transaction.model_dump(exclude_unset=True)
    transaction_db.sqlmodel_update(transaction_data)

    session.add(transaction_db)
    session.commit()
    session.refresh(transaction_db)

    return BaseResponse(
        result_code=200,
        result_message="Transaction updated successfully",
        data=transaction_db
    )


@router.delete("/{id}", response_model=BaseResponse[None])
async def delete_transaction(id: str, session: Session = Depends(get_session)):
    """
    Delete a transaction by ID.
    """
    transaction = session.get(Transaction, id)
    if not transaction:
        raise AppHTTPException(
            result_code=404,
            result_message="Transaction not found",
            error_code="E404"
        )

    session.delete(transaction)
    session.commit()

    return BaseResponse(
        result_code=200,
        result_message="Transaction deleted successfully",
    )
