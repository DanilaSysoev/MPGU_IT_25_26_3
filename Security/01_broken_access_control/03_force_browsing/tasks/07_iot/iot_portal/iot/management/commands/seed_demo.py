# iot/management/commands/seed_demo.py
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from iot.models import Device, LogFile, User

DEMO_USERS = [
    {"username":"admin","email":"admin@iot.local","is_staff":True,"is_superuser":True,"is_tech":True,"password":"password"},
    {"username":"tech_tom","email":"tom@iot.local","is_staff":True,"is_superuser":False,"is_tech":True,"password":"password"},
    {"username":"owner_jane","email":"jane@iot.local","is_staff":False,"is_superuser":False,"is_tech":False,"password":"password"},
]

SAMPLE_LOG = b"Device log for device %s\nOwner: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for iot app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding iot demo...")
            users = self._create_users()
            owners = [u for u in users if not getattr(u, "is_tech", False)]
            created_devices = []
            created_logs = []
            for i, owner in enumerate(owners, start=1):
                d, _ = Device.objects.get_or_create(owner=owner, serial=f"SN-{i:04d}", defaults={"name": f"Device {i}"})
                created_devices.append(d)
                lf = LogFile(device=d)
                fname = f"{d.serial}_log.txt"
                lf.filename = fname
                lf.file.save(fname, ContentFile(SAMPLE_LOG % (d.serial.encode(), owner.username.encode())), save=True)
                created_logs.append(lf)
                self.stdout.write(f"  + device {d.serial} log -> {lf.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("IoT demo seeded."))

    def _create_users(self) -> list[User]:
        out = []
        for cfg in DEMO_USERS:
            u, created = User.objects.get_or_create(username=cfg["username"], defaults={"email": cfg["email"]})
            changed = False
            if created:
                u.set_password(cfg["password"])
                changed = True
            for f in ("is_staff","is_superuser"):
                if getattr(u, f) != cfg[f]:
                    setattr(u, f, cfg[f])
                    changed = True
            if hasattr(u, "is_tech") and getattr(u, "is_tech") != cfg.get("is_tech", False):
                setattr(u, "is_tech", cfg.get("is_tech", False))
                changed = True
            if changed:
                u.save()
                self.stdout.write(self.style.SUCCESS(f"  + user {u.username}"))
            else:
                self.stdout.write(f"  = user {u.username} (unchanged)")
            out.append(u)
        return out

    def _create_static_backup(self):
        static_dirs = getattr(settings, "STATICFILES_DIRS", [])
        target = static_dirs[0] if static_dirs else os.path.join(settings.BASE_DIR, "static")
        os.makedirs(os.path.join(target, "backups"), exist_ok=True)
        with open(os.path.join(target, "backups", ".env.backup"), "wb") as f:
            f.write(b"IOT_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
