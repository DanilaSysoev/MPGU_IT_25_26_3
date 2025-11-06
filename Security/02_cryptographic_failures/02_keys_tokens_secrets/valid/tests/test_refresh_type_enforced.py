import auth
import storage
import user

def test_refresh_endpoint_requires_refresh_token_type():
    user.register_user("tom", "tom@example.com", "Password123!")
    access, _ = auth.login("tom", "Password123!")
    try:
        auth.refresh_pair(access)  # передаём access туда, где ждут refresh
        assert False, "refresh_pair must reject access tokens"
    except Exception as e:
        assert "wrong token type" in str(e).lower()

    storage.clear_data()