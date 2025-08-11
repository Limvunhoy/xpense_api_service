from pydantic import BaseModel, ConfigDict, Field
from typing import Generic, TypeVar, Optional
from datetime import datetime, timezone


T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]): 
    result_code: int 
    result_message: str 
    data: Optional[T] = Field(default=None)
    # created_at: datetime = datetime.now(timezone.utc)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda v: v.isoformat()},
        extra="ignore",
        use_enum_values=True,
        str_strip_whitespace=True,
        str_min_length=0,
        str_max_length=255,
        arbitrary_types_allowed=True,
        exclude_none=True,  # <-- this removes `None` fields like `data`
    )

class PaginatedResponse(BaseResponse[T], Generic[T]):
    total: int
    skip: int
    limit: int

class ErrorResponse(BaseModel): 
    result_code: int 
    result_message: str
    error_code: str