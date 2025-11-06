from typing import Any, Tuple

import crypto

def record_token(payload: dict[str, Any]) -> None:
    raise NotImplementedError()

def revoke_by_jti(jti: str) -> None:
    raise NotImplementedError()

def is_revoked(jti: str) -> bool:
    raise NotImplementedError()

def is_expired(exp: str) -> bool:
    raise NotImplementedError()

def login(username: str, password: str) -> Tuple[str, str]:
    raise NotImplementedError()

def verify_access(access: str) -> dict[str, Any]:
    raise NotImplementedError()

def refresh_pair(refresh_token: str) -> Tuple[str, str]:
    raise NotImplementedError()

def revoke(token: str) -> None:
    raise NotImplementedError()

def introspect(token: str) -> dict[str, Any]:
    try:
        payload = crypto.decode(token)
        active = (not is_revoked(payload["jti"])) and (not is_expired(payload["exp"]))
        return {
            "active": active,
            "sub": payload.get("sub"),
            "typ": payload.get("typ"),
            "exp": payload.get("exp"),
            "jti": payload.get("jti"),
        }
    except Exception:
        return {"active": False, "error": "invalid_token"}
