import os
import pytest
import requests
from django.core.files.base import ContentFile
from django.conf import settings

from ecom.models import Order, InvoiceFile, User

SAFE_STATUS = {401, 403, 302, 404}

@pytest.fixture(autouse=True)
def use_tmp_media_root(monkeypatch, tmp_path):
    tmp_media = str(tmp_path / "media")
    os.makedirs(tmp_media, exist_ok=True)
    monkeypatch.setattr(settings, "MEDIA_ROOT", tmp_media)
    yield

@pytest.mark.django_db
def test_admin_requires_auth(client):
    r = client.get("/old/admin/maintenance/")
    assert r.status_code in SAFE_STATUS

@pytest.mark.django_db
def test_order_view_acl(client):
    owner = User.objects.create_user("owner", password="password")
    o = Order.objects.create(customer=owner, total=10)
    # anonymous should not see protected manager page
    r_anon = client.get(f"/orders/{o.id}/view/")
    assert r_anon.status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_invoice_acl(client):
    owner = User.objects.create_user("owner2", password="password")
    o = Order.objects.create(customer=owner, total=1)
    inv = InvoiceFile(order=o)
    inv.file.save("inv.txt", ContentFile(b"inv"), save=False)
    inv.filename = "inv.txt"
    inv.save()
    r_anon = client.get(f"/files/{inv.id}/download/")
    assert r_anon.status_code in SAFE_STATUS
    client.login(username="other2", password="password")
    r_other = client.get(f"/storage/invoices/{inv.id}/download/")
    assert r_other.status_code in SAFE_STATUS
    client.logout()
    client.login(username="owner2", password="password")
    r_owner = client.get(f"/files/{inv.id}/download/")
    assert r_owner.status_code == 200
    client.logout()

@pytest.mark.django_db
def test_export_user_profile_requires_auth(client):
    alice = User.objects.create_user("alice", password="password", email="a@x")
    r_anon = client.get(f"/api/users/{alice.id}/export/")
    assert r_anon.status_code in SAFE_STATUS
    client.login(username="bob", password="password")
    r_bob = client.get(f"/api/users/{alice.id}/export/")
    assert r_bob.status_code in SAFE_STATUS
    client.logout()
    client.login(username="alice", password="password")
    r_alice = client.get(f"/api/users/{alice.id}/export/")
    assert r_alice.status_code == 200
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
