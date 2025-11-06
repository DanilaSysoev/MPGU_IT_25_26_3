import auth
import storage
import user
import crypto

def test_tokens_have_required_claims():
    user.register_user("zoe", "zoe@example.com", "Password123!")
    access, refresh = auth.login("zoe", "Password123!")

    a = crypto.decode(access)
    r = crypto.decode(refresh)

    for p, typ in [(a, "access"), (r, "refresh")]:
        assert p["iss"]
        assert p["sub"] == "zoe"
        assert isinstance(p["iat"], int)
        assert isinstance(p["exp"], int)
        assert p["jti"]
        assert p["typ"] == typ

    storage.clear_data()