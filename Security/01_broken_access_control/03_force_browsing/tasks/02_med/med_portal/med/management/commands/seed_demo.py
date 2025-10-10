# clinic/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from med.models import Patient, MedicalReport, User

DEMO_USERS = [
    {"username":"admin","email":"admin@clinic.local","is_staff":True,"is_superuser":True,"is_doctor":True,"password":"password"},
    {"username":"dr_alice","email":"alice@clinic.local","is_staff":True,"is_superuser":False,"is_doctor":True,"password":"password"},
    {"username":"charlie","email":"charlie@clinic.local","is_staff":False,"is_superuser":False,"is_doctor":False,"password":"password"},
]

SAMPLE_REPORT = b"Medical report for patient %s\nUploaded by: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for clinic app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding clinic demo...")
            users = self._create_users()
            doctors = [u for u in users if getattr(u, "is_doctor", False)]
            if not doctors: doctors = [users[0]] if users else []

            patients = []
            reports = []
            demo_patient_names = [("Ivan Petrov","1980-01-01"),("Maria Ivanova","1990-05-12")]
            for i, (name, dob) in enumerate(demo_patient_names, start=1):
                owner = doctors[i % len(doctors)]
                p, _ = Patient.objects.get_or_create(full_name=name, defaults={"dob":dob, "created_by": owner})
                patients.append(p)
                # add 1 report
                r = MedicalReport(patient=p)
                fname = f"{p.full_name.replace(' ','_')}_report.txt"
                r.filename = fname
                r.file.save(fname, ContentFile(SAMPLE_REPORT % (p.full_name.encode(), owner.username.encode())), save=True)
                reports.append(r)
                self.stdout.write(f"  + patient {p.full_name} report -> {r.file.name}")

            self._create_static_backup()

            self.stdout.write(self.style.SUCCESS("Users: " + ", ".join(u.username for u in users)))
            self.stdout.write("Patients: " + ", ".join(p.full_name for p in patients))
            self.stdout.write(self.style.SUCCESS("Clinic demo seeded."))

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
            if hasattr(u, "is_doctor") and getattr(u, "is_doctor") != cfg.get("is_doctor", False):
                setattr(u, "is_doctor", cfg.get("is_doctor", False)); changed = True
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
            f.write(b"CLINIC_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
