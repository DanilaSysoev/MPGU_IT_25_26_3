from django.test import TestCase
from django.contrib.auth.models import User
from .models import Order as Order
from .models import Invoice as Invoice

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Order.objects.create(owner=cls.dev, title='Dev Order A')
        Order.objects.create(owner=cls.mod, title='Mod Order X')
        Invoice.objects.create(owner=cls.dev, title='Dev Invoice A')
        Invoice.objects.create(owner=cls.mod, title='Mod Invoice X')


    def test_order_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Order.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/order/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_order_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Order.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/order/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_order_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Order.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/order/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_invoice_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Invoice.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/invoice/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_invoice_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Invoice.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/invoice/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_invoice_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Invoice.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/invoice/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/order/list/")
        self.assertIn(r.status_code, (302,403))
