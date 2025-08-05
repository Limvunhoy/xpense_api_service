from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session

from app.schemas.account import AccountCreate, AccountRead, AccountUpdate
from app.models.account import Account

from app.schemas.response import BaseResponse
from app.core.helper.success_response import success_response
from app.exceptions import AppHTTPException

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.get("/", response_model=BaseResponse[List[AccountRead]])
async def get_accounts(session: Session = Depends(get_session)):
    """
    Retrieve all accounts.
    """
    statement = select(Account)
    accounts = session.exec(statement).all()
    return success_response(data=accounts)


@router.post("/", response_model=BaseResponse[AccountRead], status_code=status.HTTP_201_CREATED)
async def create_account(account: AccountCreate, session: Session = Depends(get_session)):
    statement = select(Account).where(
        Account.account_number == account.account_number)
    existing_account = session.exec(statement).first()

    if existing_account:
        # raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST, detail="Account already exists")
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Account already exists",
            error_code="E404"
        )

    new_account = Account(**account.model_dump())

    session.add(new_account)
    session.commit()

    session.refresh(new_account)
    # return new_account
    return success_response(data=new_account)


@router.patch("/{id}", response_model=BaseResponse[AccountRead])
async def update_account(id: str, account: AccountUpdate, session: Session = Depends(get_session)):
    account_db = session.get(Account, id)
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found!")
    account_data = account.model_dump(exclude_unset=True)
    account_db.sqlmodel_update(account_data)
    session.add(account_db)
    session.commit()
    session.refresh(account_db)
    # return account_db
    return success_response(data=account_db)


@router.delete("/{id}")
async def delete_account(id: str, session: Session = Depends(get_session)):
    account_db = session.get(Account, id)
    if not account_db:
        raise HTTPException(status_code=404, detail="Account not found!")
    session.delete(account_db)
    session.commit()
    return {"message": "Account deleted"}
