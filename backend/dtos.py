import datetime
from dataclasses import dataclass
from typing import List


@dataclass
class Profile:
    first_name: str
    last_name: str
    email: str
    username: str
    phone_number: str
    occupation: str
    address: str
    password: str
    confirm_password: str


@dataclass
class Login:
    id: str
    full_name: str
    email: str
    username: str


# Response Model
@dataclass
class BaseResponse:
    status: bool
    message: str


@dataclass
class LoginResponseModel(BaseResponse):
    token: str
    full_name: str


# Request Models
@dataclass
class LoginRequestModel:
    username: str
    password: str
