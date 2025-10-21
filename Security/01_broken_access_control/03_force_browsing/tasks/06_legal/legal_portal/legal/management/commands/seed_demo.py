# legal/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from legal.models import Case, CaseDocument, User

DEMO_USERS = [
    {"username":"admin","email":"admin@legal.local","is_staff":True,"is_superuser":True,"is_lawyer":True,"password":"password"},
    {"username":"law_alex","email":"alex@legal.local","is_staff":True,"is_superuser":False,"is_lawyer":True,"password":"password"},
    {"username":"client_carl","email":"carl@legal.local","is_staff":False,"is_superuser":False,"is_lawyer":False,"password":"password"},
]

SAMPLE_DOC = b"Case doc for case %s\nClient: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for legal app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding legal demo...")
            users = self._create_users()
            lawyers = [u for u in users if getattr(u, "is_lawyer", False)]
            clients = [u for u in users if not getattr(u, "is_lawyer", False)]
            for i, client in enumerate(clients, start=1):
                c, _ = Case.objects.get_or_create(title=f"Case {i}", client=client)
                doc = CaseDocument(case=c)
                fname = f"case_{c.id}_doc.txt"
                doc.filename = fname
                doc.file.save(fname, ContentFile(SAMPLE_DOC % (c.title.encode(), client.username.encode())), save=True)
                self.stdout.write(f"  + case {c.title} doc -> {doc.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("Legal demo seeded."))

    def _create_users(self) -> List[User]:
        out = []
        for cfg in DEMO_USERS:
            u, created = User.objects.get_or_create(username=cfg["username"], defaults={"email": cfg["email"]})
            changed = False
            if created:
                u.set_password(cfg["password"]); changed = True
            for f in ("is_staff","is_superuser"):
                if getattr(u, f) != cfg[f]:
                    setattr(u, f, cfg[f]); changed = True
            if hasattr(u, "is_lawyer") and getattr(u, "is_lawyer") != cfg.get("is_lawyer", False):
                setattr(u, "is_lawyer", cfg.get("is_lawyer", False)); changed = True
            if changed:
                u.save(); self.stdout.write(self.style.SUCCESS(f"  + user {u.username}, password: `{cfg['password']}`"))
            else:
                self.stdout.write(f"  = user {u.username} (unchanged)")
            out.append(u)
        return out

    def _create_static_backup(self):
        static_dirs = getattr(settings, "STATICFILES_DIRS", [])
        target = static_dirs[0] if static_dirs else os.path.join(settings.BASE_DIR, "static")
        os.makedirs(os.path.join(target, "backups"), exist_ok=True)
        with open(os.path.join(target, "backups", ".env.backup"), "wb") as f:
            f.write(b"LEGAL_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
