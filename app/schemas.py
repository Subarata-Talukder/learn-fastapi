from datetime import datetime
from tokenize import String
from typing import Optional
from fastapi.security import base
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


# User schema
class UserBase(BaseModel):
    email: EmailStr
    is_active: bool

class User(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Post schema
class BasePost(BaseModel):
    title: str
    content: str
    published:bool = True
    #rating:Optional[int] = None

class Post(BasePost):
    pass

class PostResponse(BasePost):
    id: int
    created_at: datetime
    user_: UserResponse

    class Config: # make this class as Response Model
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config: # make this class as Response Model
        orm_mode = True


# JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Vote Schema
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # 0 or 1