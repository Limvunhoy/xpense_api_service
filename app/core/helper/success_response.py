from typing import Optional, TypeVar
from app.schemas.response import BaseResponse

T = TypeVar("T")

def success_response(data: Optional[T] = None, message: str = "Success") -> BaseResponse[T]:
    if data is not None:
        return BaseResponse(result_code=200, result_message=message, data=data)
    return BaseResponse(result_code=200, result_message=message)
