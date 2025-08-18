from fastapi import APIRouter, Body, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import select
from sqlmodel import Session
from app.core.settings import settings
from app.core.security import (
    ALGORITHM,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password
)
from app.database import get_session
from app.exceptions import AppHTTPException
from app.models.user import User
from app.schemas.base_response import BaseResponse
from app.schemas.user import UserCreate, UserLogin, UserRead, UserWithToken
from app.core.helper.success_response import success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", response_model=BaseResponse[UserWithToken])
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(
        User.username == user_data.username)).first()
    if existing_user:
        raise AppHTTPException(
            result_code=status.HTTP_400_BAD_REQUEST,
            result_message="Username already exists",
            error_code="E400"
        )

    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    access_token = create_access_token({"sub": new_user.id})
    refresh_token = create_refresh_token(new_user.id, new_user.token_version)

    return success_response(
        data=UserWithToken(
            id=new_user.id,
            username=new_user.username,
            email=new_user.email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    )


@router.post("/login", response_model=BaseResponse[UserWithToken])
def login(request: UserLogin, session: Session = Depends(get_session)):
    user = session.scalars(select(User).where(
        User.username == request.username)).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise AppHTTPException(
            result_code=status.HTTP_401_UNAUTHORIZED,
            result_message="Invalid credentials",
            error_code="E401"
        )

    # Optional: update last login
    user.last_login = user.last_login  # or datetime.now(timezone.utc)
    session.add(user)
    session.commit()

    access_token = create_access_token({"sub": user.id})
    refresh_token = create_refresh_token(user.id, user.token_version)

    return success_response(
        data=UserWithToken(
            id=user.id,
            username=user.username,
            email=user.email,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    )


@router.post("/refresh", response_model=BaseResponse[UserWithToken])
def refresh_token(refresh_token: str = Body(...), session: Session = Depends(get_session)):
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        token_version = payload.get("token_version")
    except JWTError:
        raise AppHTTPException(
            result_code=status.HTTP_401_UNAUTHORIZED,
            result_message="Invalid refresh token",
            error_code="E401"
        )

    user = session.get(User, user_id)
    if not user or user.token_version != token_version:
        raise AppHTTPException(
            result_code=status.HTTP_401_UNAUTHORIZED,
            result_message="Refresh token revoked",
            error_code="E401"
        )

    # Rotate refresh token
    user.token_version += 1
    session.add(user)
    session.commit()

    access_token = create_access_token({"sub": user.id})
    new_refresh_token = create_refresh_token(user.id, user.token_version)

    return success_response(
        data=UserWithToken(
            id=user.id,
            username=user.username,
            email=user.email,
            access_token=access_token,
            refresh_token=new_refresh_token,
            token_type="bearer"
        )
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = AppHTTPException(
        result_code=status.HTTP_401_UNAUTHORIZED,
        result_message="Could not validate credentials",
        error_code="E401",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY,
                             algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
    except JWTError as e:
        print("JWT Error:", e)
        raise credentials_exception

    try: 
        user_id = int(user_id_str)
    except ValueError:
        raise credentials_exception

    user = session.get(User, user_id)
    if not user:
        raise credentials_exception
    return user


@router.get("/me", response_model=BaseResponse[UserRead])
def read_user_current(current_user: User = Depends(get_current_user)):
    return success_response(
        data=UserRead(
            id=current_user.id,
            username=current_user.username,
            email=current_user.email
        )
    )
