import pytest

def test_missing_secret_raises_on_use(monkeypatch):
    import crypto
    bckp = crypto.JWT_SECRET
    crypto.JWT_SECRET = ""
    with pytest.raises(RuntimeError):
        crypto.issue_access("alice")
    crypto.JWT_SECRET = bckp
