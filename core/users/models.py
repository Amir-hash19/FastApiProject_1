from sqlalchemy import Column, String, Boolean, func, Integer, DateTime
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
from datetime import datetime



pwd_context = CryptContext(schemes=["argon2"],deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    national_id = Column(Integer,nullable=False)
    updated_date = Column(DateTime(),default=datetime.now,onupdate=datetime.now)

    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")


    def hash_password(self, plain_password: str) -> str:
        return pwd_context.hash(plain_password)
    

    def verify_password(self, plain_password: str)-> bool:
        return pwd_context.verify(plain_password, self.password)
    

    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)
        


    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, full_name={self.full_name})>"
    



