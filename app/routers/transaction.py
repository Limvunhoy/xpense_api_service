from fastapi import APIRouter, Depends, Query, status
from typing import List, Optional
from sqlalchemy import func
from sqlmodel import Session, select, desc
from sqlalchemy.orm import selectinload

from app.database import get_session
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.schemas.transaction import TransactionRead, TransactionCreate, TransactionUpdate
from app.schemas.base_response import BaseResponse, PaginatedResponse
from app.exceptions import AppHTTPException
from app.core.helper.success_response import success_response, paginated_success_response
from datetime import datetime

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=PaginatedResponse[List[TransactionRead]])
def get_transactions(
    *,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    account_id: Optional[str] = Query(None),
    category_id: Optional[str] = Query(None),
    currency: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
):
    """
    Retrieve all transactions. 
    """
    try:
        statement = select(Transaction)

        if account_id:
            statement = statement.where(Transaction.account_id == account_id)
        if category_id:
            statement = statement.where(Transaction.category_id == category_id)
        if currency:
            statement = statement.where(Transaction.currency == currency)
        if date_from:
            statement = statement.where(
                Transaction.transaction_date >= date_from)
        if date_to:
            statement = statement.where(
                Transaction.transaction_date <= date_to)

        statement = statement.order_by(desc(Transaction.transaction_date))

        count_statement = select(
            func.count()).select_from(statement.subquery())
        total = session.exec(count_statement).one()

        transactions = session.exec(statement.offset(skip).limit(limit)).all()

        return paginated_success_response(
            data=transactions,
            total=total,
            skip=skip,
            limit=limit,
        )

        # return success_response(data=transactions or [])
    except Exception as e:
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to fetch transactions",
            error_code="E500",
        )


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

    return success_response(data=transaction)


@router.post("/", response_model=BaseResponse[TransactionRead], status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_in: TransactionCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new transaction.
    """
    try:
        account = session.get(Account, transaction_in.account_id)
        if not account:
            raise AppHTTPException(
                result_code=status.HTTP_404_NOT_FOUND,
                result_message="Account does not exist",
                error_code="E404"
            )

        category = session.get(Category, transaction_in.category_id)
        if not category:
            raise AppHTTPException(
                result_code=status.HTTP_404_NOT_FOUND,
                result_message="Category does not exist",
                error_code="E404"
            )

        new_transaction = Transaction(**transaction_in.model_dump())
        session.add(new_transaction)
        session.commit()
        session.refresh(new_transaction)

        return success_response(
            result_code=status.HTTP_201_CREATED,
            result_message="Success",
            data=new_transaction,
        )
    except AppHTTPException:
        raise
    except Exception as e:
        print(e)
        session.rollback()
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to create transaction",
            error_code="E500",
        )


@router.patch("/{id}", response_model=BaseResponse[TransactionRead])
async def update_transaction(
    id: str,
    transaction_in: TransactionUpdate,
    session: Session = Depends(get_session)
):
    """
    Update an existing transaction by ID.
    """
    try:
        transaction_db = session.get(Transaction, id)
        if not transaction_db:
            raise AppHTTPException(
                result_code=404,
                result_message="Transaction not found",
                error_code="E404"
            )

        update_data = transaction_in.model_dump(exclude_unset=True)
        transaction_db.sqlmodel_update(update_data)

        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)

        return success_response(data=transaction_db)
    except AppHTTPException as e:
        session.rollback()
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to update transaction",
            error_code="E500",
            detail=str(e)
        )


@router.delete("/{id}", response_model=BaseResponse[None])
async def delete_transaction(id: str, session: Session = Depends(get_session)):
    """
    Delete a transaction by ID.
    """
    try:
        transaction = session.get(Transaction, id)
        if not transaction:
            raise AppHTTPException(
                result_code=404,
                result_message="Transaction not found",
                error_code="E404"
            )

        session.delete(transaction)
        session.commit()

        return success_response()
    except AppHTTPException as e:
        session.rollback()
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to delete transaction",
            error_code="E500",
            detail=str(e)
        )
