import os
import pytest
import requests
from django.core.files.base import ContentFile
from django.conf import settings
from lms.models import Course, Assignment, Submission, User

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
def test_submission_view_acl(client):
    instructor = User.objects.create_user("inst", password="password")
    student = User.objects.create_user("stu", password="password")
    course = Course.objects.create(title="C")
    course.instructors.add(instructor)
    a = Assignment.objects.create(course=course, title="A")
    s = Submission(assignment=a, student=student)
    s.file.save("s.txt", ContentFile(b"x"), save=False)
    s.filename="s.txt"
    s.save()
    assert client.get(f"/assignments/{s.id}/").status_code in SAFE_STATUS

@pytest.mark.django_db
def test_download_submission_acl(client):
    student = User.objects.create_user("stu2", password="password")
    course = Course.objects.create(title="C2")
    assignment = Assignment.objects.create(course=course, title="A2")
    sub = Submission(assignment=assignment, student=student)
    sub.file.save("sub.txt", ContentFile(b"x"), save=False)
    sub.filename="sub.txt"
    sub.save()
    assert client.get(f"/files/{sub.id}/download/").status_code in SAFE_STATUS
    client.login(username="other2", password="password")
    assert client.get(f"/storage/submissions/{sub.id}/download/").status_code in SAFE_STATUS
    client.logout()
    client.login(username="stu2", password="password")
    assert client.get(f"/files/{sub.id}/download/").status_code == 200
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
