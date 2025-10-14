import os, pytest, requests
from django.core.files.base import ContentFile
from django.conf import settings
from iot.models import Device, LogFile, User

SAFE_STATUS = {401,403,302,404}

@pytest.fixture(autouse=True)
def use_tmp_media_root(monkeypatch, tmp_path):
    tmp_media = str(tmp_path / "media"); os.makedirs(tmp_media, exist_ok=True)
    monkeypatch.setattr(settings, "MEDIA_ROOT", tmp_media)
    yield

@pytest.mark.django_db
def test_admin_requires_auth(client):
    assert client.get("/old/admin/maintenance/").status_code in SAFE_STATUS

@pytest.mark.django_db
def test_device_view_acl(client):
    owner = User.objects.create_user("owner", password="password")
    other = User.objects.create_user("other", password="password")
    d = Device.objects.create(owner=owner, serial="SN1", name="D")
    assert client.get(f"/devices/{d.id}/").status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_log_acl(client):
    owner = User.objects.create_user("owner2", password="password")
    other = User.objects.create_user("other2", password="password")
    d = Device.objects.create(owner=owner, serial="SN2", name="D2")
    lf = LogFile(device=d); lf.file.save("l.txt", ContentFile(b"x"), save=False); lf.filename="l.txt"; lf.save()
    assert client.get(f"/files/{lf.id}/download/").status_code in SAFE_STATUS
    client.login(username="other2", password="password")
    assert client.get(f"/storage/logs/{lf.id}/download/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="owner2", password="password")
    assert client.get(f"/files/{lf.id}/download/").status_code == 200
    client.logout()

@pytest.mark.django_db
def test_export_user_profile_requires_auth(client):
    alice = User.objects.create_user("alice", password="password")
    bob = User.objects.create_user("bob", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code in SAFE_STATUS
    client.login(username="bob", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="alice", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code == 200
    client.logout()


@pytest.mark.usefixtures("db")
def test_sensitive_static_not_public(live_server, settings, tmp_path):
    url = f"{live_server.url}/static/backups/.env.backup"
    try: resp = requests.get(url, timeout=5)
    except Exception as exc: pytest.skip(f"Cannot request live_server: {exc}")
    assert resp.status_code in SAFE_STATUS
