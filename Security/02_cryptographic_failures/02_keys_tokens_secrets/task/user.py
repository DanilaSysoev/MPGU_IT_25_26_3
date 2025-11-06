from dataclasses import dataclass, asdict
from typing import Optional, Any
from passlib.context import CryptContext
import storage

@dataclass
class User:
    username: str
    email: str
    password_hash: str
    failed_attempts: int = 0
    locked_until: float | None = None

    def to_record(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_record(cls, rec: dict[str, Any]) -> "User":
        return cls(**rec)

def get_user(username: str) -> Optional[User]:
    db = storage.load_users()
    for rec in db["users"]:
        if rec["username"] == username:
            return User.from_record(rec)
    return None

def save_user(u: User) -> None:
    db = storage.load_users()
    for i, rec in enumerate(db["users"]):
        if rec["username"] == u.username:
            db["users"][i] = u.to_record()
            storage.save_users(db)
            return
    db["users"].append(u.to_record())
    storage.save_users(db)

def user_exists(username: str) -> bool:
    return get_user(username) is not None

def register_user(username: str, email: str, password: str) -> User:
    if user_exists(username):
        raise ValueError("user exists")
    ctx = CryptContext(schemes=["bcrypt"])
    ph = ctx.hash(password)
    u = User(username=username, email=email, password_hash=ph)
    save_user(u)
    return u

def verify_password(u: User, password: str) -> bool:
    ctx = CryptContext(schemes=["bcrypt"])
    return ctx.verify(password, u.password_hash)
