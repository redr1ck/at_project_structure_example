from pydantic import BaseModel
from enum import StrEnum
from typing import List
from pydantic.types import AwareDatetime


class Genders(StrEnum):
    MALE = 'male'
    FEMALE = 'female'


class BaseResponse(BaseModel):
    isSuccess: bool
    errorCode: int
    errorMessage: str | None


class UserData(BaseModel):
    id: int
    name: str
    gender: Genders
    age: int
    city: str
    registrationDate: AwareDatetime


class UserResponse(BaseResponse):
    user: UserData | None


class UsersResponse(BaseResponse):
    idList: List[int]

