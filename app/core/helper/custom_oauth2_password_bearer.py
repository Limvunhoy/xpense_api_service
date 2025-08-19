from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer

from app.exceptions import AppHTTPException


class CustomOAuth2PasswordBearer(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> str:
        authorization: str = request.headers.get("Authorization")

        # Handle missing Authorization header
        if not authorization:
            # Instead of returning JSONResponse directly (FastAPI expects str here),
            # raise an HTTPException so FastAPI handles it properly
            raise AppHTTPException(
                result_code=status.HTTP_401_UNAUTHORIZED,
                result_message="Unauthorized: Token is missing",
                error_code="E401",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return await super().__call__(request)
