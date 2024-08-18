import random

from sqlalchemy.orm import Session

from db import crud
from db.redis import get_redis
from db.settings import OTP_LEN, OTP_EX_TIME, OTP_FAILED_TIMES
from schemas import UserBase


def send_otp(phone: str) -> str:
    otp_code = ''.join(random.choices('0123456789', k=OTP_LEN))
    print(otp_code)
    # TODO send otp code with sms
    print(f'otp sent [{otp_code} -> {phone}]')
    redis = get_redis()
    redis.set(phone, f'{otp_code}:*', ex=OTP_EX_TIME)
    return otp_code


def verify_otp(phone: str, otp_code: str) -> (bool, str):
    redis = get_redis()
    cache_result = redis.get(phone)
    if cache_result:
        correct_otp_code, failed_attempts = cache_result.split(':')
        if correct_otp_code == otp_code:
            redis.delete(phone)
            return True, 'OK'
        else:
            if len(failed_attempts) < OTP_FAILED_TIMES:
                redis.set(phone, f'{cache_result}*', redis.ttl(phone))
            else:
                redis.delete(phone)
            return False, f'Invalid otp'
    else:
        return False, f'otp expired'


def login_user(phone: str) -> dict:
    #  TODO return access and refresh jwt token
    return {
        'access': 'access token',
        'refresh': 'refresh token',
    }


def get_user(phone: str, db: Session) -> UserBase:
    user = crud.get_user(phone=phone, db=db)
    return user


def get_or_create_user(phone: str, db: Session) -> UserBase:
    user = get_user(phone=phone, db=db)
    if not user:
        user = crud.create_user(phone=phone, db=db)
    return user
