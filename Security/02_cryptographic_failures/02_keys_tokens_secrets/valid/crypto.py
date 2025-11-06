import os
import uuid
from typing import Any, Tuple
from dotenv import load_dotenv
import jwt
from datetime import datetime, timedelta, timezone

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
ACCESS_TTL_MIN = int(os.getenv("ACCESS_TTL_MIN", "15"))
REFRESH_TTL_DAYS = int(os.getenv("REFRESH_TTL_DAYS", "7"))
ISSUER = os.getenv("ISSUER", "auth-cli")

def _require_secret():
    if not JWT_SECRET:
        raise RuntimeError("JWT_SECRET not configured (.env)")

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def make_jti() -> str:
    return str(uuid.uuid4())

def _encode(payload: dict[str, Any]) -> str:
    _require_secret()
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def _decode(token: str) -> dict[str, Any]:
    _require_secret()
    return jwt.decode(
        token, JWT_SECRET, algorithms=["HS256"],
        options={"require": ["exp","iat","iss","sub","jti","typ"]}
    )

def issue_access(sub: str, scope: list[str] | None = None) -> Tuple[str, dict[str, Any]]:
    iat = now_utc()
    exp = iat + timedelta(minutes=ACCESS_TTL_MIN)
    payload = {
        "iss": ISSUER,
        "sub": sub,
        "iat": int(iat.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": make_jti(),
        "typ": "access",
        "scope": scope or ["profile:read"],
    }
    return _encode(payload), payload

def issue_refresh(sub: str) -> Tuple[str, dict[str, Any]]:
    iat = now_utc()
    exp = iat + timedelta(days=REFRESH_TTL_DAYS)
    payload = {
        "iss": ISSUER,
        "sub": sub,
        "iat": int(iat.timestamp()),
        "exp": int(exp.timestamp()),
        "jti": make_jti(),
        "typ": "refresh",
    }
    return _encode(payload), payload

def decode(token: str) -> dict[str, Any]:
    return _decode(token)
