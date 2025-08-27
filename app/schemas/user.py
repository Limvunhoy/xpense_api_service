from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        froM_attribute = True


class UserWithToken(BaseModel):
    id: int
    username: str
    email: EmailStr
    access_token: str
    refresh_token: str
    token_type: str

    class Config:
        froM_attribute = True

class RefreshTokenRequest(BaseModel):
    refresh_token: str