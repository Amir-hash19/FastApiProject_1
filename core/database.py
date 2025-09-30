from sqlalchemy import create_engine, Column, String, Integer, DateTime ,Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from passlib.context import CryptContext
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                    connect_args={"check_same_thread": False}
                       )



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


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
    



class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Numeric(10, 2))
    created_at = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="payments")

    def __repr__(self):
        return f"<Payment(id={self.id}, user_id={self.user_id}, amount={self.amount})>"
    


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()    
