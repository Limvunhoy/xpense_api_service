from typing import Optional, TypeVar, List, Union
from app.schemas.base_response import BaseResponse, PaginatedResponse

T = TypeVar("T")


def success_response(
    result_code: int = 200,
    data: Optional[Union[T, List[T]]] = None,
    result_message: str = "Success"
) -> BaseResponse[Union[T, List[T]]]:
    return BaseResponse(result_code=result_code, result_message=result_message, data=data)

    # if data is not None:
    #     return BaseResponse(result_code=result_code, result_message=message, data=data)
    # return BaseResponse(result_code=200, result_message=message)


def paginated_success_response(
        data: Optional[Union[T, List[T]]] = None,
        total: int = 0,
        skip: int = 0,
        limit: int = 0,
        result_code: int = 200,
        result_message: str = "Success",
) -> PaginatedResponse[Union[T, List[T]]]:
    return PaginatedResponse(
        result_code=result_code,
        result_message=result_message,
        data=data,
        total=total,
        skip=skip, # control pagination (offset)
        limit=limit, # control pagination
    )
