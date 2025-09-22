from sqlalchemy import create_engine, Column, String, Integer, DateTime ,Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL,
                    connect_args={"check_same_thread": False}
                       )



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()





class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.now)
    national_id = Column(Integer,nullable=False)
    updated_date = Column(DateTime(),default=datetime.now,onupdate=datetime.now)


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