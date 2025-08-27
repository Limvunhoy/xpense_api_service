from enum import Enum


class AppErrorCode(str, Enum):
    INVALID_CREDENTIALS= "E401"     # wrong username or password
    ACCESS_TOKEN_EXPIRED="E402"     # expired / invalid access token
    REFRESH_TOKEN_INVALID = "E403"  # invalid / revoked refresh token

    # User related 
    USER_NOT_FOUND="E404"
    USER_ALREADY_EXIST="E405"

    # Validation 
    INVALID_REQUEST="E422"

    # Server / DB
    INVALID_ERROR = "E500"
    DATABASE_ERROR = "E501"