from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ticket as Ticket
from .models import Message as Message

class IdorLessonTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_staff=True, is_superuser=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Ticket.objects.create(owner=cls.dev, title='Dev Ticket A')
        Ticket.objects.create(owner=cls.mod, title='Mod Ticket X')
        Message.objects.create(owner=cls.dev, text='Dev Message A')
        Message.objects.create(owner=cls.mod, text='Mod Message X')


    def test_ticket_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Ticket.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/ticket/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_ticket_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Ticket.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/ticket/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_ticket_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Ticket.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/ticket/update/{other.id}/", data={'title':'HACK'})
        self.assertIn(r.status_code, (401,403))


    def test_message_access_by_query_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Message.objects.filter(owner=self.mod).first()
        r = self.client.get("/vuln/message/", {'id': other.id})
        self.assertEqual(r.status_code, 403)

    def test_message_access_by_path_must_be_denied_after_fix(self):
        self.client.login(username="dev", password="devpass123")
        other = Message.objects.filter(owner=self.mod).first()
        r = self.client.get(f"/vuln/message/path/{other.id}/")
        self.assertEqual(r.status_code, 403)

    def test_message_update_must_require_ownership(self):
        self.client.login(username="dev", password="devpass123")
        other = Message.objects.filter(owner=self.mod).first()
        r = self.client.post(f"/vuln/message/update/{other.id}/", data={'text':'HACK'})
        self.assertIn(r.status_code, (401,403))

    def test_unauthenticated_access_redirect(self):
        r = self.client.get("/secure/ticket/list/")
        self.assertIn(r.status_code, (302,403))
