from fastapi import APIRouter

from schemas import SendOTPInput, VerifyOTPInput
from services import send_otp, verify_otp

# from customers.routers import users_router


router = APIRouter()


@router.post('/send-otp/')
def send_otp_api(data: SendOTPInput):
    otp = send_otp(data.phone)
    return {'data': data, 'otp': otp}


@router.post('/verify-otp/')
def verify_otp_api(data: VerifyOTPInput):
    result, message = verify_otp(data.phone, data.otp_code)
    return {'result': result, 'message': message}


@router.get('/user/{phone}/')
def get_user_information(phone: str):
    pass
