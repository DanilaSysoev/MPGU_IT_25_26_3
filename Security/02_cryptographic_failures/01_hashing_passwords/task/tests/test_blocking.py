from user import InMemoryUserStorage
import auth


def test_new_user_lock_flag_is_false():
    store = InMemoryUserStorage()
    auth.register_user(store, "alice", "alice@example.com", "Password123!")

    assert auth.is_account_locked(store, "alice") is False


def test_lock_flag_turns_true_after_5_failures():
    store = InMemoryUserStorage()
    auth.register_user(store, "bob", "bob@example.com", "Password123!")

    # До 5 неудачных логинов флаг — False
    for _ in range(4):
        assert auth.verify_credentials(store, "bob", "wrong-pass") is False
        assert auth.is_account_locked(store, "bob") is False

    # Пятая неудача — пользователь блокируется
    assert auth.verify_credentials(store, "bob", "still-wrong") is False
    assert auth.is_account_locked(store, "bob") is True


def test_locked_user_cannot_login_even_with_correct_password():
    store = InMemoryUserStorage()
    auth.register_user(store, "carol", "carol@example.com", "Password123!")

    # Набиваем 5 неудачных попыток, чтобы уйти в блокировку
    for _ in range(5):
        assert auth.verify_credentials(store, "carol", "nope") is False

    assert auth.is_account_locked(store, "carol") is True

    # Даже верный пароль при блокировке — не пускает
    assert auth.verify_credentials(store, "carol", "Password123!") is False
    assert auth.is_account_locked(store, "carol") is True
