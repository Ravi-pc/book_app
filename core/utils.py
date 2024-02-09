import logging
from datetime import datetime, timedelta
import bcrypt
import jwt
from sanic import response, Request
from sqlalchemy import select
from core.model import User
from core.settings import jwt_secrete_key, sender, password, super_key
from core.model import async_session

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = jwt_secrete_key
Sender = sender
Password = password
super_key = super_key

logging.basicConfig(filename='./book_store.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%y %I:%M:%S %p')
logger = logging.getLogger()


def hash_password(plain_password: str) -> str:
    """
        Description: hash_password function is used to hash the password.
        Parameter: normal password.
        Return: hashed password.
    """
    hashed_password_bytes = bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password_bytes.decode('utf-8')
    return hashed_password_str


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict):
    """
        Description: create_access_token function to create the token.

        Parameter: data in the dictionary format.

        Return: token.

    """
    expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expires_delta})
    encoded_jwt = jwt.encode(data, JWT_SECRET_KEY, algorithm=ALGORITHM)
    # print(encoded_jwt)
    return encoded_jwt


def decode_token(token):
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])


async def authorize(request: Request):
    token = request.token

    if not token:
        return response.json({"message": "Unauthorized: Missing Authorization Header"}, status=401)

    try:
        decoded_token = decode_token(token)
        user_id = decoded_token.get('user_id')

        # Add user information to request state for later use
        request.ctx.user_id = user_id

    except Exception as e:
        return response.json({"message": f"Unauthorized: {str(e)}"}, status=401)
