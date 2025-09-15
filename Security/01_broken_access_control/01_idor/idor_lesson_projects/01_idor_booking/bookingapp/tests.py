from django.test import TestCase
from django.contrib.auth.models import User
from .models import Booking as Booking
from .models import Payment as Payment

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Booking.objects.create(owner=cls.dev, title='Dev Booking A')
        Booking.objects.create(owner=cls.mod, title='Mod Booking X')
        Payment.objects.create(owner=cls.dev, title='Dev Payment A')
        Payment.objects.create(owner=cls.mod, title='Mod Payment X')


    def test_booking_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Booking.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/booking/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_booking_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Booking.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/booking/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_booking_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Booking.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/booking/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_payment_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Payment.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/payment/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_payment_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Payment.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/payment/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_payment_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Payment.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/payment/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/booking/list/")
        self.assertIn(r.status_code, (302,403))
