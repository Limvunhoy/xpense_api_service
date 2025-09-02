from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel import Session, select
from typing import List
from app.database import get_session

from app.models.user import User
from app.routers.user import get_current_user
from app.schemas.wallet import AccountCreate, AccountDelete, AccountRead, AccountUpdate
from app.models.wallet import Wallet

from app.schemas.base_response import BaseResponse
from app.core.helper.success_response import success_response
from app.exceptions import AppHTTPException
from typing import Optional

router = APIRouter(prefix="/wallets", tags=["Wallets"])


@router.get("/", response_model=BaseResponse[List[AccountRead]])
async def get_wallets(
    *,
    is_active: Optional[bool] = Query(None),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all wallets.
    """
    try:
        active_filter = is_active if is_active is not None else True
        statement = select(Wallet).where(
            Wallet.user_id == current_user.id,
            Wallet.is_active == active_filter,
        )
        statement = statement.order_by(Wallet.wallet_type)

        wallets = session.exec(statement).all()
        return success_response(data=wallets)
    except Exception as e:
        raise AppHTTPException(
            result_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            result_message="Failed to fetch transactions",
            error_code="E500",
        )


@router.post("/", response_model=BaseResponse[AccountRead], status_code=status.HTTP_201_CREATED)
async def create_wallet(
    wallet_in: AccountCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    statement = select(Wallet).where(
        Wallet.user_id == current_user.id,
        Wallet.wallet_number == wallet_in.wallet_number,
    )
    existing_wallet = session.exec(statement).first()
    if existing_wallet:
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Wallet already exists",
            error_code="E400"
        )

    new_wallet = Wallet(**wallet_in.model_dump(), user_id=current_user.id)
    session.add(new_wallet)
    session.commit()
    session.refresh(new_wallet)
    return success_response(data=new_wallet)


@router.patch("/{id}", response_model=BaseResponse[AccountRead])
async def update_wallet(
    id: str,
    wallet: AccountUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    wallet_db = session.get(Wallet, id)
    if not wallet_db or not wallet_db.is_active or wallet_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=status.HTTP_404_NOT_FOUND,
            result_message="Wallet not found",
            error_code="E404"
        )

    wallet_data = wallet.model_dump(exclude_unset=True)
    wallet_db.sqlmodel_update(wallet_data)
    session.add(wallet_db)
    session.commit()
    session.refresh(wallet_db)
    return success_response(data=wallet_db)


@router.post("/delete")
async def delete_wallet(
    *,
    request: AccountDelete,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    wallet_db = session.get(Wallet, request.wallet_id)
    if not wallet_db or not wallet_db.is_active or wallet_db.user_id != current_user.id:
        raise AppHTTPException(
            result_code=status.HTTP_404_NOT_FOUND,
            result_message="Wallet not found",
            error_code="E404"
        )

    wallet_db.is_active = False
    session.add(wallet_db)
    session.commit()
    session.refresh(wallet_db)
    return success_response()
