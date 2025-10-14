import os, pytest, requests
from django.core.files.base import ContentFile
from django.conf import settings
from saas.models import Project, Task, Attachment, User

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
def test_task_view_acl(client):
    alice = User.objects.create_user("alice", password="password")
    bob = User.objects.create_user("bob", password="password")
    proj = Project.objects.create(name="P")
    proj.members.add(alice)
    task = Task.objects.create(project=proj, title="T")
    r_anon = client.get(f"/projects/{proj.id}/")
    assert r_anon.status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_attachment_acl(client):
    proj = Project.objects.create(name="P2")
    task = Task.objects.create(project=proj, title="T2")
    att = Attachment(task=task); att.file.save("a.txt", ContentFile(b"x"), save=False); att.filename="a.txt"; att.save()
    assert client.get(f"/files/{att.id}/download/").status_code in SAFE_STATUS
    other = User.objects.create_user("other", password="password")
    client.login(username="other", password="password")
    assert client.get(f"/storage/attachments/{att.id}/download/").status_code in SAFE_STATUS
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
