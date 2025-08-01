import jinja2

from ..decorators import register_template
from ..email_types import EmailType
from .email_base import EmailBase


@register_template(EmailType.OTP)
class OTPTemplate(EmailBase):
    def __init__(self, otp: int, valid_time: str, username: str) -> None:
        super().__init__()
        self.otp = otp
        self.valid_time = valid_time
        self.username = username
        self.email_subject = "Your OTP Code - Action Required"
        self.email_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Your OTP Code</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        p {
            line-height: 1.6;
        }
        h2 {
            color: #4CAF50;
            font-size: 24px;
        }
        .email-container {
            background-color: #ffffff;
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .footer {
            font-size: 12px;
            color: #777;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <p>Dear {{ username }},</p>
        <p>Your One-Time Password (OTP) is:</p>
        <h2>{{ otp }}</h2>
        <p>Please use this code to complete your verification. This code is valid for {{ valid_time }}.</p>
        <p>If you did not request this, please ignore this email.</p>
        <p>Thank you,</p>
        <p>Your Company Team</p>
        <div class="footer">
            <p>This is an automated message. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

    @property
    def subject(self) -> str:
        return self.email_subject

    @property
    def html(self) -> str:
        template = jinja2.Template(self.email_html)
        return template.render(
            otp=self.otp, valid_time=self.valid_time, username=self.username
        )

    @staticmethod
    def check_args(args: dict):
        if not all(key in args for key in ["otp", "valid_time", "username"]):
            raise ValueError(
                "'otp', 'valid_time', and 'username' must be present in the arguments dictionary."
            )
