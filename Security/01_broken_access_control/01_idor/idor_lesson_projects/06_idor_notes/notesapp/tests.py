from django.test import TestCase
from django.contrib.auth.models import User
from .models import Note as Note
from .models import Category as Category

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Note.objects.create(owner=cls.dev, title='Dev Note A')
        Note.objects.create(owner=cls.mod, title='Mod Note X')
        Category.objects.create(owner=cls.dev, name='Dev Category A')
        Category.objects.create(owner=cls.mod, name='Mod Category X')


    def test_note_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Note.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/note/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_note_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Note.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/note/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_note_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Note.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/note/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_category_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Category.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/category/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_category_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Category.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/category/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_category_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Category.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/category/update/{other.id}/", data={'name':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/note/list/")
        self.assertIn(r.status_code, (302,403))
