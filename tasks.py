import ssl
from email.message import EmailMessage
import smtplib
from celery import Celery
from core.settings import sender, password
from core.utils import logger

app = Celery(
    'tasks',
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0'
)

app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True

)

e_mail = EmailMessage()


@app.task()
def email_verification(token: str, user_email):
    """
        Description: email_verification function is used to send the verification link
                        to the registered user e-mail id.

        Parameter: token, user_email.

        Return: None.

    """

    sender_email = sender
    sender_password = password
    subject = 'Email Verification'
    body = f"Click the link to verify your email: http://127.0.0.1:8000/verify_user?token={token}"
    e_mail['From'] = sender_email
    e_mail['To'] = user_email
    e_mail['Subject'] = subject
    e_mail.set_content(body)
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, user_email, e_mail.as_string())
            print("Successfully")
            smtp.quit()

    except Exception as ex:
        logger.exception(ex)
