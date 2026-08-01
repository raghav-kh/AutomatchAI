import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.core.database import Base, get_db
from app import models  # noqa: F401
from app.main import app
from app.api.deps import require_admin
from app.models.user import User

TEST_DATABASE_URL = "sqlite:///:memory:"

FAKE_ADMIN = User(id=0, username="test-admin", hashed_password="unused", is_admin=True)


@pytest.fixture()
def db_session():
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """
    Default test client: DB overridden to the in-memory test session, and
    admin auth bypassed (returns a fake admin) so existing tests can focus
    on their own behavior rather than needing a token on every call.
    Real auth behavior is exercised separately in tests/test_auth.py via
    `raw_client`, which does NOT bypass auth.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[require_admin] = lambda: FAKE_ADMIN
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def raw_client(db_session):
    """Test client with real auth enforced -- only DB is overridden."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
