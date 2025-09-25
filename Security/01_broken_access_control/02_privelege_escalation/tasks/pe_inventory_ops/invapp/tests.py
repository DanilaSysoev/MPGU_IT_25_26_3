from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile

class PrivEscTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user("adminroot", password="adminroot123", is_superuser=True, is_staff=True)
        cls.dev = User.objects.create_user("dev", password="devpass123")
        cls.mod = User.objects.create_user("mod", password="modpass123")
        Profile.objects.create(user=cls.admin, role="admin")
        Profile.objects.create(user=cls.dev, role="user")
        Profile.objects.create(user=cls.mod, role="moderator")

    def test_delete_user_requires_admin(self):
        self.client.login(username="dev", password="devpass123")
        r = self.client.get("/vuln/delete_user/1/")
        self.assertEqual(r.status_code, 403, "Должна быть серверная проверка роли для удаления пользователей")

    def test_admin_panel_requires_admin(self):
        self.client.login(username="dev", password="devpass123")
        r = self.client.get("/vuln/admin_panel/")
        self.assertEqual(r.status_code, 403, "Нельзя полагаться на UI — сервер должен проверять роль")

    def test_promote_user_must_not_trust_request_role(self):
        self.client.login(username="dev", password="devpass123")
        r = self.client.get("/vuln/promote_user/2/?role=admin")
        self.assertEqual(r.status_code, 403, "RBAC не должен доверять параметрам запроса; только админ может менять роли")
