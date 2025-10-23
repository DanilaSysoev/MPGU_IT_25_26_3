import pytest
import auth
from user import InMemoryUserStorage, User

def _expected_delay(n: int) -> float:
    """
    Формула из условия: 1.5^n + 1, где n >= 1 — номер текущей подряд идущей неудачной попытки.
    Для n == 0 задержка должна быть 0.
    """
    if n <= 0:
        return 0.0
    return (1.5 ** n) + 1.0


def test_new_user_delay_is_zero():
    """
    Флаг/показатель задержки у НОВОГО пользователя должен быть 0.
    """
    store = InMemoryUserStorage()
    auth.register_user(store, "alice", "alice@example.com", "Password123!")

    u = User.load(store, "alice")
    assert u is not None
    # ожидаем пользовательское поле с задержкой == 0.0
    assert getattr(u, "backoff_seconds", None) is not None, "Ожидаем поле backoff_seconds в модели User"
    assert u.backoff_seconds == pytest.approx(0.0, rel=1e-5)


def test_delay_increases_by_formula_on_each_failed_attempt(monkeypatch):
    """
    До 5 попыток — задержка растёт по формуле, рассчитанной от количества подряд неудачных попыток.
    Проверяем и сам показатель пользователя, и то, что time.sleep() вызывается не меньше этой задержки.
    """
    store = InMemoryUserStorage()
    auth.register_user(store, "bob", "bob@example.com", "Password123!")

    slept = []

    def fake_sleep(seconds):
        # копим все переданные задержки; самих пауз не делаем
        slept.append(seconds)

    # перехватываем time.sleep внутри модуля auth
    monkeypatch.setattr("auth.time.sleep", fake_sleep)

    # n = 1..5 — прогоняем 5 неверных попыток
    for n in range(1, 6):
        assert auth.verify_credentials(store, "bob", "WRONG") is False

        u = User.load(store, "bob")
        assert u is not None

        expected = _expected_delay(n)
        # показатель задержки, сохранённый у пользователя
        assert getattr(u, "backoff_seconds", None) is not None, "Ожидаем поле backoff_seconds в модели User"
        assert u.backoff_seconds == pytest.approx(expected, rel=1e-5)

        # последняя переданная в sleep задержка — не меньше требуемой
        assert slept, "Ожидали вызов time.sleep()"
        assert slept[-1] + 1e-5 >= expected, f"sleep({slept[-1]}) < required({expected}) при n={n}"


def test_response_time_respects_user_delay(monkeypatch):
    """
    «Время ответа соответствует задержке (не меньше её)» — проверяем через перехват sleep.
    Для одной неудачной попытки убеждаемся, что переданная задержка >= расчётной, и
    что после успешного логина задержка у пользователя сбрасывается в 0.
    """
    store = InMemoryUserStorage()
    auth.register_user(store, "carol", "carol@example.com", "Password123!")

    captured = {"last_sleep": None}

    def fake_sleep(seconds):
        captured["last_sleep"] = seconds

    monkeypatch.setattr("auth.time.sleep", fake_sleep)

    # первая неудача -> n=1, ожидаем 1.5^1 + 1 = 2.5
    assert auth.verify_credentials(store, "carol", "NOPE") is False

    u = User.load(store, "carol")
    assert u is not None

    expected = _expected_delay(1)
    assert u.backoff_seconds == pytest.approx(expected, rel=1e-5)
    assert captured["last_sleep"] is not None
    assert captured["last_sleep"] + 1e-12 >= expected

    # успешный логин должен сбросить показатель задержки
    assert auth.verify_credentials(store, "carol", "Password123!") is True
    u2 = User.load(store, "carol")
    assert u2 is not None
    assert u2.backoff_seconds == pytest.approx(0.0, rel=0, abs=1e-6)
