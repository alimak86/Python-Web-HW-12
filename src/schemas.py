from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


class ResponseContactModel(BaseModel):
  id: int = Field(default=1, ge=1)
  firstname: str = Field(max_length=50)
  secondname: str = Field(max_length=50)
  email: str = Field(max_length=50)
  phonenumber: str = Field(max_length=50)
  dateofbirth: str = Field(max_length=50)


class ContactModel(BaseModel):
  firstname: str = Field(max_length=50)
  secondname: str = Field(max_length=50)
  email: str = Field(max_length=50)
  phonenumber: str = Field(max_length=50)
  dateofbirth: str = Field(max_length=50)


class ContactModelFullName(BaseModel):
  firstname: str = Field(max_length=50)
  secondname: str = Field(max_length=50)


class UserModel(BaseModel):
  username: str = Field(min_length=5, max_length=16)
  email: str
  password: str = Field(min_length=6, max_length=10)


"""
User response models
"""


class UserDb(BaseModel):
  id: int
  username: str
  email: str
  created_at: datetime
  avatar: str

  class Config:
    orm_mode = True


class UserResponse(BaseModel):
  user: UserDb
  detail: str = "User successfully created"


class TokenModel(BaseModel):
  access_token: str
  refresh_token: str
  token_type: str = "bearer"
