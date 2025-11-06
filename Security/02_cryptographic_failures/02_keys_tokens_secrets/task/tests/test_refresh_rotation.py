import auth
import storage
import user

def test_refresh_rotates_and_revokes_old():
    user.register_user("bob", "bob@example.com", "Password123!")
    access1, refresh1 = auth.login("bob", "Password123!")

    access2, refresh2 = auth.refresh_pair(refresh1)
    assert access2 != access1
    assert refresh2 != refresh1

    # старый refresh должен быть отозван
    try:
        auth.refresh_pair(refresh1)
        assert False, "expected old refresh to be revoked"
    except Exception as e:
        assert "revoked" in str(e).lower()

    storage.clear_data()