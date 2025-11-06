import auth
import storage
import user

def test_login_issues_both_tokens_and_me_ok():
    user.register_user("alice", "alice@example.com", "Password123!")
    access, refresh = auth.login("alice", "Password123!")
    assert isinstance(access, str) and access
    assert isinstance(refresh, str) and refresh

    payload = auth.verify_access(access)
    assert payload["sub"] == "alice"
    assert payload["typ"] == "access"

    storage.clear_data()