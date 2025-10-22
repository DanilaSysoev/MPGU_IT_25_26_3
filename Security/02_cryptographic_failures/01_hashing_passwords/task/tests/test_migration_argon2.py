import hashlib
from passlib.context import CryptContext

from user import InMemoryUserStorage, User
from auth import verify_credentials, register_user


def test_md5_user_is_migrated_to_argon2_on_successful_login(monkeypatch):
    store = InMemoryUserStorage()

    username = "alice"
    raw = "password123"
    md5_hex = hashlib.md5(raw.encode()).hexdigest()
    User(username=username, email="alice@example.com", password_hash=md5_hex).save(store)

    assert verify_credentials(store, username, raw) is True

    migrated = User.load(store, username)
    assert migrated is not None

    ctx = CryptContext(schemes=["argon2"])
    assert ctx.verify(raw, migrated.password_hash)


def test_register_stores_argon2_hash(monkeypatch):
    store = InMemoryUserStorage()

    _ = register_user(store, "alice", "alice@example.com", "S3curePass!")
    saved = User.load(store, "alice")
    assert saved is not None

    ctx = CryptContext(schemes=["argon2"])
    assert ctx.verify("S3curePass!", saved.password_hash)
