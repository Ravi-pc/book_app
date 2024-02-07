from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    user_name: str
    password: str = Field(max_length=255)


class UserDetails(UserLogin):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr
    phone: int
    city: str
    state: str
    super_key: Optional[str] = None


class BookSchema(BaseModel):
    book_name: str
    author: str
    price: int
    quantity: int


class CartItemsSchema(BaseModel):
    book_id: int
    quantity: int
