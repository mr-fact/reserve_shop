import random
import uuid
from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from db import crud
from db.redis import get_redis
from db.settings import OTP_LEN, OTP_EX_TIME, OTP_FAILED_TIMES
from schemas import UserBase, UserUpdateInput
from settings import JWT_ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, JWT_ALGORITHM, JWT_PRIVATE_KEY, JWT_PUBLIC_KEY


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


def get_user_by_id(user_id: int, db: Session) -> UserBase:
    user = crud.get_user_by_id(user_id=user_id, db=db)
    return user


def update_user_by_id(user_id: int, user_info: UserUpdateInput, db: Session) -> UserBase:
    return crud.update_user_by_id(user_id, user_info, db)


def get_or_create_user(phone: str, db: Session) -> UserBase:
    user = get_user(phone=phone, db=db)
    if not user:
        user = crud.create_user(phone=phone, db=db)
    return user


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        'token_type': 'access',
        'exp': int(expire.timestamp()),
        'iat': int(datetime.now().timestamp()),
        'jti': str(uuid.uuid4()),
        'user_id': str(user_id),
    }
    encoded_jwt = jwt.encode(to_encode, JWT_PRIVATE_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, db: Session) -> UserBase:
    try:
        payload = jwt.decode(token, JWT_PUBLIC_KEY, algorithms=JWT_ALGORITHM)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail='Token expired!!!!!')
    user_id: int = payload.get("user_id")
    user = get_user_by_id(user_id, db)
    return user
