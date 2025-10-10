import os
import pytest
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from med.models import Patient, MedicalReport, User

SAFE_STATUS = {401,403,302,404}

@pytest.fixture(autouse=True)
def use_tmp_media_root(monkeypatch, tmp_path):
    tmp_media = str(tmp_path / "media")
    os.makedirs(tmp_media, exist_ok=True)
    monkeypatch.setattr(settings, "MEDIA_ROOT", tmp_media)
    yield

@pytest.mark.django_db
def test_admin_requires_auth(client):
    assert client.get("/old/admin/maintenance/").status_code in SAFE_STATUS

@pytest.mark.django_db
def test_patient_view_acl(client):
    owner = User.objects.create_user("owner", password="password")
    p = Patient.objects.create(full_name="X", dob="1990-01-01", created_by=owner)
    r_anon = client.get(f"/patients/{p.id}/")
    assert r_anon.status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_report_acl(client):
    owner = User.objects.create_user("owner2", password="password")
    p = Patient.objects.create(full_name="Y", dob="1980-01-01", created_by=owner)
    rpt = MedicalReport(patient=p)
    rpt.file.save("r1.txt", ContentFile(b"r"), save=False)
    rpt.filename="r1.txt"
    rpt.save()
    assert client.get(f"/files/{rpt.id}/download/").status_code in SAFE_STATUS
    client.login(username="other2", password="password")
    assert client.get(f"/storage/reports/{rpt.id}/download/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="owner2", password="password")
    assert client.get(f"/files/{rpt.id}/download/").status_code == 200
    client.logout()

@pytest.mark.django_db
def test_export_user_profile_requires_auth(client):
    alice = User.objects.create_user("alice", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code in SAFE_STATUS
    client.login(username="bob", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="alice", password="password")
    assert client.get(f"/api/users/{alice.id}/export/").status_code == 200
    client.logout()


@pytest.mark.usefixtures("db")
def test_sensitive_static_not_public(live_server, settings, tmp_path):
    static_dir = tmp_path / "static_public"
    (static_dir / "backups").mkdir(parents=True)
    (static_dir / "backups" / ".env.backup").write_text("FAKE")
    settings.STATICFILES_DIRS = [str(static_dir)]
    settings.DEBUG = True
    url = f"{live_server.url}/static/backups/.env.backup"
    try:
        resp = requests.get(url, timeout=5)
    except Exception as exc:
        pytest.skip(f"Cannot request live_server: {exc}")
    assert resp.status_code in SAFE_STATUS
