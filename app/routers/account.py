from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session

from app.models.user import User
from app.routers.user import get_current_user
from app.schemas.account import AccountCreate, AccountDelete, AccountRead, AccountUpdate
from app.models.account import Account

from app.schemas.base_response import BaseResponse
from app.core.helper.success_response import success_response
from app.exceptions import AppHTTPException
from typing import Optional

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=BaseResponse[List[AccountRead]])
async def get_accounts(
    *,
    is_active: Optional[bool] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all accounts.
    """
    try:
        active_filter = is_active if is_active is not None else True
        statement = select(Account).where(
            Account.user_id == current_user.id,
            Account.is_active == active_filter,
        )
        statement = statement.order_by(Account.account_type)

        accounts = session.exec(statement).all()
        return success_response(data=accounts)
    except Exception as e:
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to fetch transactions",
            error_code="E500",
        )


@router.post("/", response_model=BaseResponse[AccountRead], status_code=status.HTTP_201_CREATED)
async def create_account(
    account_in: AccountCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Account).where(
        Account.user_id == current_user.id,
        Account.account_number == account_in.account_number,
    )
    existing_account = session.exec(statement).first()
    if existing_account:
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Account already exists",
            error_code="E400"
        )

    new_account = Account(**account_in.model_dump(), user_id=current_user.id)
    session.add(new_account)
    session.commit()
    session.refresh(new_account)
    return success_response(data=new_account)


@router.patch("/{id}", response_model=BaseResponse[AccountRead])
async def update_account(
    id: str,
    account: AccountUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    account_db = session.get(Account, id)
    if not account_db or not account_db.is_active or account_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=status.HTTP_404_NOT_FOUND,
            result_message="Account not found",
            error_code="E404"
        )

    account_data = account.model_dump(exclude_unset=True)
    account_db.sqlmodel_update(account_data)
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return success_response(data=account_db)


@router.post("/delete")
async def delete_account(
    *,
    request: AccountDelete,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    account_db = session.get(Account, request.account_id)
    if not account_db or not account_db.is_active or account_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=status.HTTP_404_NOT_FOUND,
            result_message="Account not found",
            error_code="E404"
        )

    account_db.is_active = False
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    return success_response()
