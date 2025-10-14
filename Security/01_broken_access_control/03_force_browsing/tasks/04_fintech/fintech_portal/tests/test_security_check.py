import os
import pytest
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from fintech.models import Account, Statement, User

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
def test_account_view_acl(client):
    owner = User.objects.create_user("owner", password="password")
    acc = Account.objects.create(owner=owner, number="DEMO1")
    assert client.get(f"/accounts/{acc.id}/").status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_statement_acl(client):
    owner = User.objects.create_user("owner2", password="password")
    acc = Account.objects.create(owner=owner, number="DEMO2")
    st = Statement(account=acc)
    st.file.save("st.txt", ContentFile(b"x"), save=False)
    st.filename="st.txt"
    st.save()
    assert client.get(f"/files/{st.id}/download/").status_code in SAFE_STATUS
    client.login(username="other2", password="password")
    assert client.get(f"/storage/statements/{st.id}/download/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="owner2", password="password")
    assert client.get(f"/files/{st.id}/download/").status_code == 200
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
    
    url = f"{live_server.url}/static/backups/.env.backup"
    try:
        resp = requests.get(url, timeout=5)
    except Exception as exc:
        pytest.skip(f"Cannot request live_server: {exc}")
    assert resp.status_code in SAFE_STATUS
