from uuid import UUID
from fastapi import APIRouter, Depends, Query, logger, status
from typing import List, Optional
from sqlalchemy import func
from sqlmodel import Session, select, desc
from sqlalchemy.orm import selectinload

from app.core.helper.timezones import get_now_utc_plus_7
from app.database import get_session
from app.models.transaction import Transaction
from app.models.account import Account
from app.models.category import Category
from app.schemas.transaction import TransactionDelete, TransactionRead, TransactionCreate, TransactionUpdate
from app.schemas.base_response import BaseResponse, PaginatedResponse
from app.exceptions import AppHTTPException
from app.core.helper.success_response import success_response, paginated_success_response
from datetime import datetime, timezone, timedelta


router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=PaginatedResponse[List[TransactionRead]])
def get_transactions(
    *,
    session: Session = Depends(get_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    account_id: Optional[UUID] = Query(None),
    category_id: Optional[UUID] = Query(None),
    currency: Optional[str] = Query(None),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
):
    """
    Retrieve all transactions. 
    """
    try:
        statement = select(Transaction).where(Transaction.is_active == True)

        if account_id:
            statement = statement.where(Transaction.account_id == account_id)
        if category_id:
            statement = statement.where(Transaction.category_id == category_id)
        if currency:
            statement = statement.where(Transaction.currency == currency)
        if date_from:
            statement = statement.where(
                Transaction.transaction_date >= date_from
            )
        if date_to:
            statement = statement.where(
                Transaction.transaction_date <= date_to
            )

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


@router.get("/current-week", response_model=BaseResponse[List[TransactionRead]])
def get_current_week_transactions(
    *,
    session: Session = Depends(get_session),
    currency: Optional[str] = Query(
        "USD",
        min_length=3,
        max_length=3,
        pattern="^[A-Z]{3}$",
        description="Filter by 3-letter ISO currency code (e.g. 'USD', 'KHR')"
    ),
):
    """
    Retrieve all transactions for the current week (Monday 00:00:00 to Sunday 23:59:59) in UTC+7 timezone.

    Optionally filter by currency code. Returns transactions ordered by date (newest first).
    """
    try:
        # Get current time in UTC+7 (Phnom Penh timezone)
        tz = timezone(timedelta(hours=7))
        current_time = datetime.now(tz)

        # Calculate week boundaries
        start_of_week = current_time - timedelta(days=current_time.weekday())
        start_of_week = start_of_week.replace(
            hour=0, minute=0, second=0, microsecond=0
        )

        end_of_week = start_of_week + timedelta(days=6)
        end_of_week = end_of_week.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

        # Build base query
        query = (
            select(Transaction)
            .where(
                Transaction.transaction_date >= start_of_week,
                Transaction.transaction_date <= end_of_week
            )
            .order_by(desc(Transaction.transaction_date))
        )

        # Apply currency filter if provided
        if currency:
            query = query.where(Transaction.currency == currency.upper())

        # Execute query
        transactions = session.exec(query).all()

        return success_response(data=transactions)

    except Exception as e:
        logger.error(f"Failed to fetch current week transactions: {str(e)}")
        raise AppHTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch current week transactions",
            error_code="TRANSACTION_FETCH_ERROR",
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

    def validate_entity(entity, name: str):
        """Validate that the entity exists and it active"""
        if entity is None or not entity.is_active:
            raise AppHTTPException(
                result_code=status.HTTP_404_NOT_FOUND,
                result_message=f"{name} does not exist or is inactive",
                error_code="E404"
            )

    try:
        account = session.get(Account, transaction_in.account_id)
        validate_entity(account, "Account")

        category = session.get(Category, transaction_in.category_id)
        validate_entity(category, "Category")

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
    id: UUID,
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


# @router.delete("/{id}", response_model=BaseResponse[None])
# async def delete_transaction(id: UUID, session: Session = Depends(get_session)):
#     """
#     Delete a transaction by ID.
#     """
#     try:
#         transaction = session.get(Transaction, id)
#         if not transaction:
#             raise AppHTTPException(
#                 result_code=404,
#                 result_message="Transaction not found",
#                 error_code="E404"
#             )

#         session.delete(transaction)
#         session.commit()

#         return success_response()
#     except AppHTTPException as e:
#         session.rollback()
#         raise AppHTTPException(
#             result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             result_message="Failed to delete transaction",
#             error_code="E500",
#             detail=str(e)
#         )


@router.post("/delete")
async def delete_transaction(
    *,
    request: TransactionDelete,
    session: Session = Depends(get_session)
):
    try:
        transaction_db = session.get(Transaction, request.transaction_id)
        if not transaction_db:
            raise AppHTTPException(
                result_code=404,
                result_message="Transaction not found",
                error_code="E404"
            )

        transaction_db.is_active = False

        session.add(transaction_db)
        session.commit()
        session.refresh(transaction_db)

        return success_response()

    except Exception as e:
        session.rollback()
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to delete transaction",
            error_code="E500",
            detail=str(e)
        )
