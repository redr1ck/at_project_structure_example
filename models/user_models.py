from pydantic import BaseModel
from typing import List, Optional


class BaseResponse(BaseModel):
    isSuccess: bool
    errorCode: int
    errorMessage: Optional[str] = None


class UserData(BaseModel):
    id: int
    name: str
    gender: str
    age: int
    city: str
    registrationDate: str


class UserResponse(BaseResponse):
    user: Optional[UserData] = None


class UsersResponse(BaseResponse):
    idList: Optional[List[int]] = []

