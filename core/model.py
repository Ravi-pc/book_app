from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, BigInteger, Boolean


DataBase_Url = 'postgresql+asyncpg://postgres:ra1020@localhost:5432/book_app'
engine = create_async_engine(DataBase_Url)
Base = declarative_base()


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
