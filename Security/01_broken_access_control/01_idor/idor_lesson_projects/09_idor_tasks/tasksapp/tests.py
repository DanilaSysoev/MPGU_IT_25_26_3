from django.test import TestCase
from django.contrib.auth.models import User
from .models import Task as Task
from .models import TaskComment as TaskComment

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Task.objects.create(owner=cls.dev, title='Dev Task A')
        Task.objects.create(owner=cls.mod, title='Mod Task X')
        TaskComment.objects.create(owner=cls.dev, text='Dev TaskComment A')
        TaskComment.objects.create(owner=cls.mod, text='Mod TaskComment X')


    def test_task_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Task.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/task/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_task_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Task.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/task/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_task_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Task.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/task/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_taskcomment_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = TaskComment.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/taskcomment/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_taskcomment_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = TaskComment.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/taskcomment/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_taskcomment_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = TaskComment.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/taskcomment/update/{other.id}/", data={'text':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/task/list/")
        self.assertIn(r.status_code, (302,403))
