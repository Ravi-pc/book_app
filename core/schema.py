from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    user_name: str = Field("Enter the user name")
    password: str = Field("Enter password")


class UserDetails(UserLogin):
    first_name: str = Field("Enter the First Name", pattern=r'^[A-Z]{1}\D{3,}')
    last_name: str = Field("Enter the Last Name", pattern=r'^[A-Z]{1}\D{3,}')
    email: EmailStr
    phone: int = Field("Enter the phone Number", )
    city: str = Field("Enter the name of your city")
    state: str = Field("Enter the name of your city")
    super_key: Optional[str] = None


class BookSchema(BaseModel):
    book_name: str = Field("Enter the book name")
    author: str = Field("Enter the author name")
    price: int = Field("Enter the Price")
    quantity: int = Field("Enter the quantity of the book")


class CartItemsSchema(BaseModel):
    book_id: int = Field("Enter the book id")
    quantity: int = Field("Enter the quantity of the book")
