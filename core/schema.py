from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    password: str = Field(max_length=255)
    user_name: str


class UserDetails(UserLogin):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone: int
    city: str
    state: str
