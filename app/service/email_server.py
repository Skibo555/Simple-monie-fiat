from app.config.config import settings
from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig
from typing import List
from starlette.background import BackgroundTasks


conf = ConnectionConfig(
    MAIL_FROM=settings.SENDER_EMAIL,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.SENDER_MAIL_SERVER,
    MAIL_PASSWORD=settings.SENDER_MAIL_PASSWORD,
    MAIL_USERNAME=settings.SENDER_USERNAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)


async def send_mail(user_mail, subject, body):
    message = MessageSchema(
        subject=subject,
        recipients=user_mail,
        template_body=body,
        subtype=MessageType.plain
    )

    fm = FastMail(conf)
    await fm.send_message(message)
