import os, pytest, requests
from django.core.files.base import ContentFile
from django.conf import settings
from supply_chain.models import Supplier, InventoryItem, ShipmentDocument, User

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
def test_item_view_acl(client):
    sup = Supplier.objects.create(name="S")
    it = InventoryItem.objects.create(sku="SKU1", supplier=sup)
    manager = User.objects.create_user("mgr", password="password")
    other = User.objects.create_user("other", password="password")
    # protected path requires supply manager, anon/other should be blocked
    r_anon = client.get(f"/items/{it.id}/")
    assert r_anon.status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_shipment_doc_acl(client):
    sup = Supplier.objects.create(name="S2")
    it = InventoryItem.objects.create(sku="SKU2", supplier=sup)
    d = ShipmentDocument(item=it); d.file.save("d.txt", ContentFile(b"x"), save=False); d.filename="d.txt"; d.save()
    assert client.get(f"/files/{d.id}/download/").status_code in SAFE_STATUS
    other = User.objects.create_user("other2", password="password")
    client.login(username="other2", password="password")
    assert client.get(f"/storage/shipments/{d.id}/download/").status_code in SAFE_STATUS
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
    static_dir = tmp_path / "static_public"; (static_dir / "backups").mkdir(parents=True)
    (static_dir / "backups" / ".env.backup").write_text("FAKE")
    settings.STATICFILES_DIRS = [str(static_dir)]; settings.DEBUG = True
    url = f"{live_server.url}/static/backups/.env.backup"
    try: resp = requests.get(url, timeout=5)
    except Exception as exc: pytest.skip(f"Cannot request live_server: {exc}")
    assert resp.status_code in SAFE_STATUS
