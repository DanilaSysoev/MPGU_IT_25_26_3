# user.py
from dataclasses import dataclass
from typing import Protocol, Optional, Dict


class UserStorage(Protocol):
    def get_user(self, username: str) -> Optional[Dict]: ...
    def save_user(self, record: Dict) -> None: ...
    def exists(self, username: str) -> bool: ...


@dataclass
class User:
    username: str
    email: str
    password_hash: str

    def save(self, storage: UserStorage) -> None:
        storage.save_user({
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
        })

    @classmethod
    def load(cls, storage: UserStorage, username: str) -> Optional["User"]:
        rec = storage.get_user(username)
        if rec is None:
            return None
        return cls(**rec)

    @classmethod
    def exists(cls, storage: UserStorage, username: str) -> bool:
        return storage.exists(username)


class InMemoryUserStorage:
    """Учебное хранилище на словаре."""
    def __init__(self) -> None:
        self._db: Dict[str, Dict] = {}

    def get_user(self, username: str) -> Optional[Dict]:
        return self._db.get(username)

    def save_user(self, record: Dict) -> None:
        self._db[record["username"]] = dict(record)

    def exists(self, username: str) -> bool:
        return username in self._db
