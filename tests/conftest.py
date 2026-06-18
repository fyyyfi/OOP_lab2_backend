"""Shared pytest fixtures: an isolated in-memory database and test client."""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.main import create_app


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    app = create_app()

    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def dispatcher_token(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "disp",
            "full_name": "Disp",
            "password": "secret123",
            "role": "dispatcher",
        },
    )
    resp = client.post(
        "/api/auth/login", json={"username": "disp", "password": "secret123"}
    )
    return resp.json()["access_token"]


@pytest.fixture
def tenant_token(client):
    client.post(
        "/api/auth/register",
        json={
            "username": "ten",
            "full_name": "Ten",
            "password": "secret123",
            "role": "tenant",
        },
    )
    resp = client.post(
        "/api/auth/login", json={"username": "ten", "password": "secret123"}
    )
    return resp.json()["access_token"]
