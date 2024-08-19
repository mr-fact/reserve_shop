from fastapi import Depends
from sqlalchemy.orm import Session

from db.postgresql import get_db
from schemas import UserBase
from db import models


def get_user(phone: str, db: Session) -> UserBase:
    return db.query(models.User).filter(models.User.phone == phone).first()


def get_user_by_id(user_id: int, db: Session) -> UserBase:
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(phone: str, db: Session):
    user = models.User(phone=phone)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
