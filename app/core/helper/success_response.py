from typing import Optional, TypeVar, List, Union
from app.schemas.response import BaseResponse

T = TypeVar("T")


def success_response(
    result_code: int = 200,
    data: Optional[Union[T, List[T]]] = None,
    message: str = "Success"
) -> BaseResponse[Union[T, List[T]]]:
    return BaseResponse(result_code=result_code, result_message=message, data=data)

    # if data is not None:
    #     return BaseResponse(result_code=result_code, result_message=message, data=data)
    # return BaseResponse(result_code=200, result_message=message)
