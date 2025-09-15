from django.test import TestCase
from django.contrib.auth.models import User
from .models import Client as Client
from .models import Deal as Deal

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Client.objects.create(owner=cls.dev, name='Dev Client A')
        Client.objects.create(owner=cls.mod, name='Mod Client X')
        Deal.objects.create(owner=cls.dev, title='Dev Deal A')
        Deal.objects.create(owner=cls.mod, title='Mod Deal X')


    def test_client_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Client.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/client/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_client_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Client.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/client/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_client_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Client.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/client/update/{other.id}/", data={'name':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_deal_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Deal.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/deal/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_deal_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Deal.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/deal/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_deal_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Deal.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/deal/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/client/list/")
        self.assertIn(r.status_code, (302,403))
