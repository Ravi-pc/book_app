from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, String, BigInteger, Boolean, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from core.settings import database_path

DataBase_Url = database_path
engine = create_async_engine(DataBase_Url)
Base = declarative_base()
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):

    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    phone = Column(BigInteger)
    is_verified = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)
    book = relationship('Book', back_populates='user')
    cart = relationship('Cart', back_populates='user')

    def __repr__(self):
        return self.user_name


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='book')
    cart_items = relationship('CartItems', back_populates='book')

    def __repr__(self):
        return self.book_name


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_price = Column(Integer, default=0)
    total_quantity = Column(Integer, default=0)
    is_ordered = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = relationship('User', back_populates='cart')
    cart_items = relationship('CartItems', back_populates='cart')


class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Integer, default=0)
    quantity = Column(Integer, default=0)
    book_id = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'), nullable=False, unique=True)
    cart_id = Column(Integer, ForeignKey('cart.id', ondelete='CASCADE'), nullable=False)
    book = relationship('Book', back_populates='cart_items')
    cart = relationship('Cart', back_populates='cart_items')
