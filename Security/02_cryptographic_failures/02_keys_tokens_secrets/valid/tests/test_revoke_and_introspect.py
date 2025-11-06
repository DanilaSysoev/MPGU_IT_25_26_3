import auth
import storage
import user

def test_revoke_access_makes_it_inactive():
    user.register_user("carol", "carol@example.com", "Password123!")
    access, _ = auth.login("carol", "Password123!")

    i1 = auth.introspect(access)
    assert i1["active"] is True

    auth.revoke(access)
    i2 = auth.introspect(access)
    assert i2["active"] is False

    storage.clear_data()