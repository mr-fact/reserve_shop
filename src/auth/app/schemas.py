from pydantic import BaseModel, constr


class SendOTPInput(BaseModel):
    phone: constr(pattern=r'^\+98\d{10}$')


class VerifyOTPInput(BaseModel):
    phone: constr(pattern=r'^\+98\d{10}$')
    otp_code: constr(pattern=r'^\d{4}$')
