from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session

from app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from app.models.account import Account

from app.schemas.base_response import BaseResponse
from app.core.helper.success_response import success_response
from app.exceptions import AppHTTPException

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=BaseResponse[List[AccountRead]])
async def get_accounts(session: Session = Depends(get_session)):
    """
    Retrieve all accounts.
    """
    statement = select(Account).where(
        Account.is_active == True
    ).order_by(
        Account.account_type
    )

    accounts = session.exec(statement).all()
    return success_response(data=accounts)


@router.post("/", response_model=BaseResponse[AccountRead], status_code=status.HTTP_201_CREATED)
async def create_account(account_in: AccountCreate, session: Session = Depends(get_session)):
    """
    Create a new account.
    """
    statement = select(Account).where(
        Account.account_number == account_in.account_number
    )
    existing_account = session.exec(statement).first()

    if existing_account:
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Account already exists",
            error_code="E400"
        )

    new_account = Account(**account_in.model_dump())

    session.add(new_account)
    session.commit()
    session.refresh(new_account)

    return success_response(data=new_account)


@router.patch("/{id}", response_model=BaseResponse[AccountRead])
async def update_account(id: str, account: AccountUpdate, session: Session = Depends(get_session)):
    """
    Update an existing account.
    """
    account_db = session.get(Account, id)
    if not account_db:
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


@router.delete("/{id}")
async def delete_account(id: str, session: Session = Depends(get_session)):
    """
    Delete na account by ID. 
    """
    account_db = session.get(Account, id)
    if not account_db:
        raise AppHTTPException(
            result_code=status.HTTP_404_NOT_FOUND,
            result_message="Account not found",
            error_code="E404"
        )
    session.delete(account_db)
    session.commit()
    return success_response()
