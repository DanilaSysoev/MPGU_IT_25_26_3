from django.test import TestCase
from django.contrib.auth.models import User
from .models import Grade as Grade
from .models import Assignment as Assignment

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Grade.objects.create(owner=cls.dev, title='Dev Grade A')
        Grade.objects.create(owner=cls.mod, title='Mod Grade X')
        Assignment.objects.create(owner=cls.dev, title='Dev Assignment A')
        Assignment.objects.create(owner=cls.mod, title='Mod Assignment X')


    def test_grade_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Grade.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/grade/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_grade_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Grade.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/grade/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_grade_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Grade.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/grade/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_assignment_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Assignment.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/assignment/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_assignment_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Assignment.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/assignment/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_assignment_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Assignment.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/assignment/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/grade/list/")
        self.assertIn(r.status_code, (302,403))
