from sqlalchemy.orm import Session

from schemas import UserBase, UserUpdateInput
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


def update_user_by_id(user_id: int, user_info: UserUpdateInput, db: Session):
    user_query = db.query(models.User).filter(models.User.id == user_id)
    user_query.update(user_info.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    return user_query.first()
