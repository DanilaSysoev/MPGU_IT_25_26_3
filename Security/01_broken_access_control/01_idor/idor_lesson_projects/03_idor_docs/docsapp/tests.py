from django.test import TestCase
from django.contrib.auth.models import User
from .models import Document as Document
from .models import FileEntry as FileEntry

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Document.objects.create(owner=cls.dev, title='Dev Document A')
        Document.objects.create(owner=cls.mod, title='Mod Document X')
        FileEntry.objects.create(owner=cls.dev, name='Dev FileEntry A')
        FileEntry.objects.create(owner=cls.mod, name='Mod FileEntry X')


    def test_document_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Document.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/document/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_document_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Document.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/document/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_document_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Document.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/document/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_fileentry_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = FileEntry.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/fileentry/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_fileentry_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = FileEntry.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/fileentry/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_fileentry_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = FileEntry.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/fileentry/update/{other.id}/", data={'name':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/document/list/")
        self.assertIn(r.status_code, (302,403))
