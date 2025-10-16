# bank/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from fintech.models import Account, Statement, User

DEMO_USERS = [
    {"username":"admin","email":"admin@bank.local","is_staff":True,"is_superuser":True,"is_teller":True,"password":"password"},
    {"username":"teller_alice","email":"alice@bank.local","is_staff":True,"is_superuser":False,"is_teller":True,"password":"password"},
    {"username":"client_bob","email":"bob@bank.local","is_staff":False,"is_superuser":False,"is_teller":False,"password":"password"},
]

SAMPLE_STATEMENT = b"Bank statement for account %s\nOwner: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for bank app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding bank demo...")
            users = self._create_users()
            tellers = [u for u in users if getattr(u, "is_teller", False)]
            clients = [u for u in users if not getattr(u, "is_teller", False)]
            created_accounts = []
            created_statements = []
            for i, client in enumerate(clients, start=1):
                acct, _ = Account.objects.get_or_create(owner=client, number=f"DEMO{i:04d}")
                created_accounts.append(acct)
                st = Statement(account=acct)
                fname = f"stmt_{acct.number}.txt"
                st.filename = fname
                st.file.save(fname, ContentFile(SAMPLE_STATEMENT % (acct.number.encode(), client.username.encode())), save=True)
                created_statements.append(st)
                self.stdout.write(f"  + account {acct.number} statement -> {st.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("Bank demo seeded."))

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
            if hasattr(u, "is_teller") and getattr(u, "is_teller") != cfg.get("is_teller", False):
                setattr(u, "is_teller", cfg.get("is_teller", False)); changed = True
            if changed:
                u.save(); self.stdout.write(self.style.SUCCESS(f"  + user {u.username}, password: `{cfg["password"]}`"))
            else:
                self.stdout.write(f"  = user {u.username} (unchanged)")
            out.append(u)
        return out

    def _create_static_backup(self):
        static_dirs = getattr(settings, "STATICFILES_DIRS", [])
        target = static_dirs[0] if static_dirs else os.path.join(settings.BASE_DIR, "static")
        os.makedirs(os.path.join(target, "backups"), exist_ok=True)
        with open(os.path.join(target, "backups", ".env.backup"), "wb") as f:
            f.write(b"BANK_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
