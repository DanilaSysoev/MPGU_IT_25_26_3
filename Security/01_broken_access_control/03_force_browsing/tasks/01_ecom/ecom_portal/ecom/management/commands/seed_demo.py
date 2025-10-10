# shop/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from ecom.models import Order, InvoiceFile, User

DEMO_USERS = [
    {"username":"admin","email":"admin@shop.local","is_staff":True,"is_superuser":True,"is_mgr":True,"password":"password"},
    {"username":"mgr_alice","email":"alice@shop.local","is_staff":True,"is_superuser":False,"is_mgr":True,"password":"password"},
    {"username":"user_bob","email":"bob@shop.local","is_staff":False,"is_superuser":False,"is_mgr":False,"password":"password"},
]

SAMPLE_INVOICE = b"Demo invoice for order %d\nUploaded by: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for shop app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding shop demo...")
            users = self._create_users()
            managers = [u for u in users if getattr(u, "is_mgr", False)]
            if not managers: managers = [users[0]] if users else []
            created_orders = []
            created_invoices = []

            # create a couple of orders
            for i in range(1, 4):
                owner = managers[i % len(managers)] if managers else users[0]
                o, _ = Order.objects.get_or_create(customer=owner, total=10.0 * i)
                created_orders.append(o)
                # create 1 invoice per order
                inv = InvoiceFile(order=o)
                fname = f"order_{o.id}_invoice.txt"
                inv.filename = fname
                inv.file.save(fname, ContentFile(SAMPLE_INVOICE % (o.id, owner.username.encode())), save=True)
                created_invoices.append(inv)
                self.stdout.write(f"  + order #{o.id} invoice -> {inv.file.name}")

            # create static backup
            self._create_static_backup()

            self.stdout.write(self.style.SUCCESS("Users: " + ", ".join(u.username for u in users)))
            self.stdout.write("Orders: " + ", ".join(str(o.id) for o in created_orders))
            self.stdout.write(self.style.SUCCESS("Shop demo seeded."))

    def _create_users(self) -> List[User]:
        out = []
        for cfg in DEMO_USERS:
            u, created = User.objects.get_or_create(username=cfg["username"], defaults={"email": cfg["email"]})
            changed = False
            if created:
                u.set_password(cfg["password"])
                changed = True
            for f in ("is_staff","is_superuser"):
                if getattr(u, f) != cfg[f]:
                    setattr(u, f, cfg[f]); changed = True
            # custom flag
            if hasattr(u, "is_mgr") and getattr(u, "is_mgr") != cfg.get("is_mgr", False):
                setattr(u, "is_mgr", cfg.get("is_mgr", False)); changed = True
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
            f.write(b"SHOP_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
