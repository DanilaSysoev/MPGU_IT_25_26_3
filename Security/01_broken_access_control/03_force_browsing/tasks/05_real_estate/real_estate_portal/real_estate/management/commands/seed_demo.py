# realty/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from real_estate.models import Listing, DocFile, User

DEMO_USERS = [
    {"username":"admin","email":"admin@realty.local","is_staff":True,"is_superuser":True,"is_agent":True,"password":"password"},
    {"username":"agent_anna","email":"anna@realty.local","is_staff":True,"is_superuser":False,"is_agent":True,"password":"password"},
    {"username":"owner_bob","email":"bob@realty.local","is_staff":False,"is_superuser":False,"is_agent":False,"password":"password"},
]

SAMPLE_DOC = b"Property doc for listing %s\nOwner: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for realty app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding realty demo...")
            users = self._create_users()
            agents = [u for u in users if getattr(u, "is_agent", False)]
            owners = [u for u in users if not getattr(u, "is_agent", False)]
            created_listings = []
            created_docs = []
            for i, owner in enumerate(owners, start=1):
                l, _ = Listing.objects.get_or_create(title=f"Demo Listing {i}", owner=owner)
                created_listings.append(l)
                d = DocFile(listing=l)
                fname = f"listing_{l.id}_doc.txt"
                d.filename = fname
                d.file.save(fname, ContentFile(SAMPLE_DOC % (l.title.encode(), owner.username.encode())), save=True)
                created_docs.append(d)
                self.stdout.write(f"  + listing {l.title} doc -> {d.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("Realty demo seeded."))

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
            if hasattr(u, "is_agent") and getattr(u, "is_agent") != cfg.get("is_agent", False):
                setattr(u, "is_agent", cfg.get("is_agent", False)); changed = True
            if changed:
                u.save(); self.stdout.write(self.style.SUCCESS(f"  + user {u.username}"))
            else:
                self.stdout.write(f"  = user {u.username} (unchanged)")
            out.append(u)
        return out

    def _create_static_backup(self):
        static_dirs = getattr(settings, "STATICFILES_DIRS", [])
        target = static_dirs[0] if static_dirs else os.path.join(settings.BASE_DIR, "static")
        os.makedirs(os.path.join(target, "backups"), exist_ok=True)
        with open(os.path.join(target, "backups", ".env.backup"), "wb") as f:
            f.write(b"REALTY_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
