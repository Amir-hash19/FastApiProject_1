import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from core.database import Base, get_db
from core.main import app
from core.users.models import User
from core.auth.auth_jwt import generate_access_token

# دیتابیس in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# دیتابیس تمیز قبل از هر تست
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# override dependency
@pytest.fixture(scope="function")
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_db, None)


# کاربر احراز هویت‌شده
@pytest.fixture(scope="function")
def auth_user():
    return User(
        id=1,
        email="test@test.com",
        full_name="Test User",
        password="hashed_password",
        national_id=1234567890
    )


@pytest.fixture(scope="function")
def auth_client(client, auth_user):
    token = generate_access_token(auth_user.id)
    client.headers.update({"Authorization": f"Bearer {token}"})
    yield client




