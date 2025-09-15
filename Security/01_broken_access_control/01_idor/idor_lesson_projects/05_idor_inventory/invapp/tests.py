from django.test import TestCase
from django.contrib.auth.models import User
from .models import Product as Product
from .models import Supply as Supply

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Product.objects.create(owner=cls.dev, name='Dev Product A')
        Product.objects.create(owner=cls.mod, name='Mod Product X')
        Supply.objects.create(owner=cls.dev, title='Dev Supply A')
        Supply.objects.create(owner=cls.mod, title='Mod Supply X')


    def test_product_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Product.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/product/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_product_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Product.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/product/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_product_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Product.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/product/update/{other.id}/", data={'name':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_supply_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Supply.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/supply/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_supply_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Supply.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/supply/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_supply_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Supply.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/supply/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/product/list/")
        self.assertIn(r.status_code, (302,403))
