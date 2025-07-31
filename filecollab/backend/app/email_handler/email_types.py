from enum import Enum


class EmailType(Enum):
    OTP = "otp"  # Requires "otp" and "valid_type" in kwargs
