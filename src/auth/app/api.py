import fastapi
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import services
from db.postgresql import get_db
from schemas import SendOTPInput, VerifyOTPInput, UserOutput

# from customers.routers import users_router


router = APIRouter()


@router.post('/send-otp/')
def send_otp_api(data: SendOTPInput):
    otp = services.send_otp(data.phone)
    return {'data': data, 'otp': otp}


@router.post('/verify-otp/')
def verify_otp_api(data: VerifyOTPInput, db: Session = Depends(get_db)):
    result, message = services.verify_otp(data.phone, data.otp_code)
    if result:
        user = services.get_or_create_user(phone=data.phone, db=db)
        return {'result': result, 'message': message, 'user': user}
    else:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail=message)


@router.get('/user/{phone}/')
def get_user_information(phone: str, db: Session = Depends(get_db)):
    user = services.get_user(phone=phone, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='not found')
    return user
