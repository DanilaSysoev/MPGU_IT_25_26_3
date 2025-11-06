import pytest

def test_missing_secret_raises_on_use(monkeypatch):
    import crypto
    bckp = crypto.JWT_SECRET
    crypto.JWT_SECRET = ""
    with pytest.raises(RuntimeError) as e:
        crypto.issue_access("alice")
    assert "secret not set" in e.value.args[0]
    crypto.JWT_SECRET = bckp
