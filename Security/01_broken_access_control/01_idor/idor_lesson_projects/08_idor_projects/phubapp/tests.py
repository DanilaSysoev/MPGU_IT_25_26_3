from django.test import TestCase
from django.contrib.auth.models import User
from .models import Project as Project
from .models import WorkItem as WorkItem

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Project.objects.create(owner=cls.dev, title='Dev Project A')
        Project.objects.create(owner=cls.mod, title='Mod Project X')
        WorkItem.objects.create(owner=cls.dev, title='Dev WorkItem A')
        WorkItem.objects.create(owner=cls.mod, title='Mod WorkItem X')


    def test_project_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Project.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/project/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_project_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Project.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/project/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_project_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Project.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/project/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_workitem_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = WorkItem.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/workitem/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_workitem_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = WorkItem.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/workitem/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_workitem_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = WorkItem.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/workitem/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/project/list/")
        self.assertIn(r.status_code, (302,403))
