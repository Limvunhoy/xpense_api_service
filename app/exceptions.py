from fastapi import HTTPException


class AppHTTPException(HTTPException):
    def __init__(
        self,
        result_code: int,
        result_message: str,
        error_code: str,
        headers: dict | None = None
    ):
        super().__init__(status_code=result_code, detail=result_message, headers=headers)
        self.error_code = error_code
