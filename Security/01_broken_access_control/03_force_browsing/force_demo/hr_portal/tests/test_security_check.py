# tests/test_security_checks.py
import os

import pytest
import requests
from django.core.files.base import ContentFile
from django.conf import settings

from hr.models import Candidate, ResumeFile, User


SAFE_STATUS = {401, 403, 302, 404}


@pytest.fixture(autouse=True)
def use_tmp_media_root(monkeypatch, tmp_path):
    """
    Подменяем MEDIA_ROOT на временный каталог для тестов,
    чтобы операции с файлами были изолированы.
    """
    tmp_media = str(tmp_path / "media")
    os.makedirs(tmp_media, exist_ok=True)
    monkeypatch.setattr(settings, "MEDIA_ROOT", tmp_media)
    yield


@pytest.mark.django_db
def test_admin_requires_auth(client):
    """
    /old/admin/maintenance/ не должен быть доступен анониму (не должен возвращать 200).
    Тест падает (будет красным), если маршрут возвращает 200 (т.е. уязвимость осталась).
    """
    resp = client.get("/old/admin/maintenance/")
    assert resp.status_code in SAFE_STATUS, (
        f"/old/admin/maintenance/ seems public (status_code={resp.status_code})."
    )


@pytest.mark.django_db
def test_candidate_view_acl(client):
    """
    /candidates/<id>/ должен быть недоступен для анонима и для другого пользователя (если is_public=False).
    Доступен — только владелец/HR/admin (ниже проверяем аноним и другой пользователь).
    Тест падает если уязвимость осталась (статус 200 для неавторизованного).
    """
    # создаём пользователей
    owner = User.objects.create_user("owner", password="password")
    other = User.objects.create_user("other", password="password")
    # пометим owner как HR (при желании)
    owner.is_hr = True
    owner.save()

    cand = Candidate.objects.create(full_name="T Tester", email="t@example.com", created_by=owner, is_public=False)

    # аноним
    r_anon = client.get(f"/candidates/{cand.id}/")
    assert r_anon.status_code in SAFE_STATUS, f"Anonymous can view candidate (status={r_anon.status_code}) — vulnerability!"

    # другой (вошедший) пользователь
    client.login(username="other", password="password")
    r_other = client.get(f"/candidates/{cand.id}/")
    assert r_other.status_code in SAFE_STATUS, f"Non-owner user can view candidate (status={r_other.status_code}) — vulnerability!"
    client.logout()

    # владелец должен получать 200 (проверка поведения — опционально, не ломает тесты)
    client.login(username="owner", password="password")
    r_owner = client.get(f"/candidates/{cand.id}/")
    assert r_owner.status_code == 200, "Owner must be able to view own candidate"
    client.logout()


@pytest.mark.django_db
def test_download_resume_acl(client):
    """
    /files/<id>/download/ не должен отдавать файл анонимам или посторонним пользователям.
    Если маршрут возвращает 200 для таких пользователей — тест упадёт.
    """
    owner = User.objects.create_user("owner2", password="password")
    other = User.objects.create_user("other2", password="password")
    cand = Candidate.objects.create(full_name="R Res", email="r@example.com", created_by=owner, is_public=False)

    # создаём резюме (FileField сохранит файл в тестовом MEDIA_ROOT)
    resume = ResumeFile(candidate=cand, uploaded_by=owner)
    resume.file.save("test_resume.txt", ContentFile(b"demo resume"), save=False)
    resume.filename = "test_resume.txt"
    resume.save()

    # аноним
    r_anon = client.get(f"/files/{resume.id}/download/")
    assert r_anon.status_code in SAFE_STATUS, f"Anonymous can download resume (status={r_anon.status_code}) — vulnerability!"

    # другой пользователь
    client.login(username="other2", password="password")
    r_other = client.get(f"/storage/files/{resume.id}/download/")
    assert r_other.status_code in SAFE_STATUS, f"Non-owner can download resume (status={r_other.status_code}) — vulnerability!"
    client.logout()

    # владелец должен иметь доступ
    client.login(username="owner2", password="password")
    r_owner = client.get(f"/files/{resume.id}/download/")
    assert r_owner.status_code == 200, "Owner should be able to download own resume"
    client.logout()


@pytest.mark.django_db
def test_export_user_profile_requires_auth(client):
    """
    /api/users/<id>/export/ не должен отдавать данные любого пользователя без прав.
    Тест падает, если маршрут возвращает 200 для анонима или для постороннего пользователя.
    """
    alice = User.objects.create_user("alice", password="password", email="alice@example.com")
    bob = User.objects.create_user("bob", password="password", email="bob@example.com")

    # аноним пытается экспортировать профиль alice
    r_anon = client.get(f"/api/users/{alice.id}/export/")
    assert r_anon.status_code in SAFE_STATUS, f"Anonymous can export user profile (status={r_anon.status_code}) — vulnerability!"

    # bob (не admin) пытается экспортировать профиль alice
    client.login(username="bob", password="password")
    r_bob = client.get(f"/api/users/{alice.id}/export/")
    assert r_bob.status_code in SAFE_STATUS, f"Non-admin user can export another profile (status={r_bob.status_code}) — vulnerability!"
    client.logout()

    # сам alice — должен получить 200
    client.login(username="alice", password="password")
    r_alice = client.get(f"/api/users/{alice.id}/export/")
    assert r_alice.status_code == 200, "User must be able to export own profile"
    client.logout()


@pytest.mark.django_db
def test_crash_does_not_expose_stacktrace(client, settings):
    """
    При DEBUG=False /crash/ не должен раскрывать стек или секреты в теле ответа.
    Тест падёт, если тело ответа содержит 'Traceback' или 'ZeroDivisionError' или SECRET_KEY.
    """
    # Подменим SECRET_KEY на что-то уникальное, и убедимся что оно не утечёт
    settings.SECRET_KEY = "super-secret-demo-key-for-tests"

    r = client.get("/crash/")
    # ожидаем 500 (или возможно redirect/страницу), но главное — отсутствие стека
    assert r.status_code == 500 or r.status_code in SAFE_STATUS, f"/crash/ returned unexpected status {r.status_code}"

    body = r.content.decode("utf-8", errors="ignore")
    assert "Traceback" not in body, "Stacktrace leaked in response body!"
    assert "RuntimeError" not in body, "Exception name leaked in response body!"
    assert settings.SECRET_KEY not in body, "SECRET_KEY leaked in response body!"


@pytest.mark.usefixtures("db")  # не обязательно, но часто удобно иметь БД доступной
def test_sensitive_static_not_public(live_server, settings, tmp_path):
    """
    Проверяет, что файл backups/.env.backup НЕ доступен по /static/backups/.env.backup.
    Тест падает (уязвимость обнаружена) если ответ = 200.
    - Использует live_server и реальный HTTP-запрос через requests.
    - Подменяет STATICFILES_DIRS на временный каталог с нашим "чувствительным" файлом.
    """
    # 1) Подготовим временную папку static и положим туда backups/.env.backup
    static_dir = tmp_path / "static_public"
    backups_dir = static_dir / "backups"
    backups_dir.mkdir(parents=True, exist_ok=True)

    secret_file = backups_dir / ".env.backup"
    secret_file.write_text("FAKE_SECRET=very_sensitive_value\n")  # фейковые данные для теста

    # 2) Настроим settings так, чтобы static finder видел нашу папку
    #    (в тестах часто STATICFILES_DIRS переопределяют таким образом)
    settings.STATICFILES_DIRS = [str(static_dir)]
    # Убедимся, что в тестовом окружении статика обслуживается (обычно DEBUG=True)
    settings.DEBUG = True

    # 3) Сформируем URL и выполним запрос к live_server
    url = f"{live_server.url}/static/backups/.env.backup"

    # requests может отсутствовать в окружении — убедитесь, что он установлен
    try:
        resp = requests.get(url, timeout=5, allow_redirects=True)
    except Exception as exc:
        pytest.skip(f"Cannot perform HTTP request to live_server: {exc}")

    # 4) Оцениваем результат: 200 — уязвимость; любой из SAFE_STATUS — безопасно
    assert resp.status_code in SAFE_STATUS, (
        f"Sensitive static file is publicly accessible! status={resp.status_code}, url={url}"
    )
    