from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from supply_chain.models import Supplier, InventoryItem, ShipmentDocument, User

DEMO_USERS = [
    {"username":"admin","email":"admin@inventory.local","is_staff":True,"is_superuser":True,"is_supply_manager":True,"password":"password"},
    {"username":"supply_sam","email":"sam@inventory.local","is_staff":True,"is_superuser":False,"is_supply_manager":True,"password":"password"},
    {"username":"vendor_v","email":"vendor@inventory.local","is_staff":False,"is_superuser":False,"is_supply_manager":False,"password":"password"},
]

SAMPLE_SHIP = b"Shipment doc for item %s\nSupplier: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for inventory app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding inventory demo...")
            suppliers = []
            items = []
            docs = []

            sup, _ = Supplier.objects.get_or_create(name="Demo Supplier")
            suppliers.append(sup)
            for i in range(1, 4):
                it, _ = InventoryItem.objects.get_or_create(sku=f"SKU-{1000+i}", supplier=sup)
                items.append(it)
                d = ShipmentDocument(item=it)
                fname = f"{it.sku}_ship.txt"
                d.filename = fname
                d.file.save(fname, ContentFile(SAMPLE_SHIP % (it.sku.encode(), sup.name.encode())), save=True)
                docs.append(d)
                self.stdout.write(f"  + item {it.sku} doc -> {d.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("Inventory demo seeded."))

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
            if hasattr(u, "is_supply_manager") and getattr(u, "is_supply_manager") != cfg.get("is_supply_manager", False):
                setattr(u, "is_supply_manager", cfg.get("is_supply_manager", False))
                changed = True
            if changed:
                u.save()
                self.stdout.write(self.style.SUCCESS(f"  + user {u.username}, password: `{cfg['password']}`"))
            else:
                self.stdout.write(f"  = user {u.username} (unchanged)")
            out.append(u)
        return out

    def _create_static_backup(self):
        static_dirs = getattr(settings, "STATICFILES_DIRS", [])
        target = static_dirs[0] if static_dirs else os.path.join(settings.BASE_DIR, "static")
        os.makedirs(os.path.join(target, "backups"), exist_ok=True)
        with open(os.path.join(target, "backups", ".env.backup"), "wb") as f:
            f.write(b"INVENTORY_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
