import logging
import smtplib
import ssl
from datetime import datetime, timedelta
from email.message import EmailMessage

import bcrypt
import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"
JWT_SECRET_KEY = "b1a61d3450299222c96086499b01f00e7963216a152294f3ba8ef81db52146fc"
Sender = "ravisingh98138@gmail.com"
Password = "mlbs qrem subb pxdv"
super_key = "7651929879"

logging.basicConfig(filename='./fundoo_notes.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s %(message)s', datefmt='%m/%d/%y %I:%M:%S %p')
logger = logging.getLogger()


def hash_password(password: str) -> str:
    """
        Description: hash_password function is used to hash the password.
        Parameter: normal password.
        Return: hashed password.
    """
    hashed_password_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
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


def email_verification(token: str, user_email):
    """
        Description: email_verification function is used to send the verification link
                        to the registered user e-mail id.

        Parameter: token, user_email.

        Return: None.

    """

    sender = Sender
    password = Password
    subject = 'Email Verification'
    body = f"Click the link to verify your email: http://127.0.0.1:8000/verify?token={token}"
    e_mail = EmailMessage()
    e_mail['From'] = sender
    e_mail['To'] = user_email
    e_mail['Subject'] = subject
    e_mail.set_content(body)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender, password)
            smtp.sendmail(sender, user_email, e_mail.as_string())
            print("Successfully")
            smtp.quit()

    except Exception as ex:
        logger.exception(ex)
