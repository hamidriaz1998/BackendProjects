import os
import smtplib
from email.message import EmailMessage

from pydantic import EmailStr
from .email_types import EmailType
from .templates import OTPTemplate

from dotenv import load_dotenv

load_dotenv()

SMTP_HOST = os.environ.get("SMTP_HOST")
SMTP_PORT = os.environ.get("SMTP_PORT")
SMTP_USER = os.environ.get("SMTP_USER")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")

if not all([SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, SENDER_EMAIL]):
    raise ValueError(
        "One or more required environment variables for email are missing or empty."
    )

SMTP_PORT = int(SMTP_PORT)


class EmailHandler:
    def __init__(self):
        self.sender_email = SENDER_EMAIL
        self.smtp_host = SMTP_HOST
        self.smtp_port = SMTP_PORT
        self.smtp_user = SMTP_USER
        self.smtp_password = SMTP_PASSWORD

    def send_email(self, receiver: EmailStr, email_type: EmailType, **kwargs):
        template = None
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = receiver

        match email_type:
            case EmailType.OTP:
                OTPTemplate.check_args(kwargs)
                template = OTPTemplate(**kwargs)

        message["Subject"] = template.subject
        message.set_content(template.html, "html")

        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(message)
