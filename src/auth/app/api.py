import fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

import services
from db.postgresql import get_db
from schemas import SendOTPInput, VerifyOTPInput, UserBase, UserUpdateInput, UserOutput

# from customers.routers import users_router


router = APIRouter()
header_scheme = APIKeyHeader(name="Authorization")


def get_current_user_by_token(token: str = Depends(header_scheme), db: Session = Depends(get_db)):
    token_data = services.verify_access_token(token, db)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"Authorization": "Bearer"},
        )

    # Fetch the user from the database using the decoded username
    user = services.get_user_by_id(user_id=token_data.id, db=db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user


@router.post('/send-otp/')
def send_otp_api(data: SendOTPInput):
    print(data.phone)
    otp = services.send_otp(data.phone)
    return {'data': data, 'otp': otp}


@router.post('/verify-otp/')
def verify_otp_api(data: VerifyOTPInput, db: Session = Depends(get_db)):
    result, message = services.verify_otp(data.phone, data.otp_code)
    if result:
        user = services.get_or_create_user(phone=data.phone, db=db)
        token = services.create_access_token(user.id)
        return {
            'result': result,
            'message': message,
            'user': user,
            'token': token
        }
    else:
        raise HTTPException(status_code=fastapi.status.HTTP_401_UNAUTHORIZED, detail=message)


@router.get('/user/me/', response_model=UserOutput)
def get_user_information(user: UserBase = Depends(get_current_user_by_token)):
    return user


@router.patch('/user/me/', response_model=UserOutput)
def update_user_information(user_info: UserUpdateInput, user: UserBase = Depends(get_current_user_by_token),
                            db: Session = Depends(get_db)):
    return services.update_user_by_id(user.id, user_info, db)


@router.get('/user/{phone}/')
def get_user_information(phone: str, db: Session = Depends(get_db)):
    user = services.get_user(phone=phone, db=db)
    if not user:
        raise HTTPException(status_code=404, detail='not found')
    return user
