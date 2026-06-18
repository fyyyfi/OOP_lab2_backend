"""Unit tests for password hashing and JWT helpers."""
import pytest
from jose import JWTError

from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)


def test_password_hash_roundtrip():
    hashed = hash_password("secret123")
    assert hashed != "secret123"
    assert verify_password("secret123", hashed)
    assert not verify_password("wrong", hashed)


def test_jwt_roundtrip():
    token = create_access_token(subject="alice", role="dispatcher")
    claims = decode_access_token(token)
    assert claims["sub"] == "alice"
    assert claims["role"] == "dispatcher"


def test_invalid_token_rejected():
    with pytest.raises(JWTError):
        decode_access_token("not-a-real-token")
