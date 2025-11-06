import os
import jwt
import time
import auth
import user
import crypto
import storage

def test_invalid_signature_rejected(monkeypatch):
    user.register_user("dave", "dave@example.com", "Password123!")
    access, _ = auth.login("dave", "Password123!")

    pl = crypto.decode(access)
    forged = jwt.encode(pl, "WRONG_SECRET", algorithm="HS256")
    try:
        auth.verify_access(forged)
        assert False, "should not verify with wrong signature"
    except Exception as e:
        assert "signature" in str(e).lower() or "token" in str(e).lower()
    
    storage.clear_data()
    

def test_expired_access_is_rejected():
    user.register_user("erin", "erin@example.com", "Password123!")
    access, _ = auth.login("erin", "Password123!")

    pl = crypto.decode(access)
    pl["exp"] = int(time.time()) - 1
    expired = jwt.encode(pl, os.getenv("JWT_SECRET"), algorithm="HS256")
    try:
        auth.verify_access(expired)
        assert False, "expected expired token rejection"
    except Exception as e:
        assert "expired" in str(e).lower() or "token" in str(e).lower()

    storage.clear_data()