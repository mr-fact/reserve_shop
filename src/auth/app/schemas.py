from typing import Optional

from pydantic import BaseModel, constr, EmailStr


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


class UserOutput(BaseModel):
    id: int
    phone: str
    name: str
    email: str
    is_active: bool
    is_admin: bool


class UserUpdateInput(BaseModel):
    name: Optional[constr(max_length=20)] = None
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True
