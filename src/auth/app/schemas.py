from pydantic import BaseModel, constr


class SendOTPInput(BaseModel):
    phone: constr(pattern=r'^\+98\d{10}$')


class VerifyOTPInput(BaseModel):
    phone: constr(pattern=r'^\+98\d{10}$')
    otp_code: constr(pattern=r'^\d{4}$')


class UserBase(BaseModel):
    phone: constr(pattern=r'^\+98\d{10}$')


class UserCreate(UserBase):
    name: str = constr(min_length=1, max_length=100)
    email: str


class UserOutput(UserBase):
    name: str
