from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session

from db.postgresql import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone = Column(String(20), unique=True, nullable=False)
    name = Column(String(20), default='')
    email = Column(String(50), default='')
    password = Column(String(50), default='')
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    def create(self, db: Session):
        db.add(self)
        db.commit()
        db.refresh(self)
