# lms/management/commands/seed_demo.py
from typing import Optional, List
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from lms.models import Course, Assignment, Submission, User

DEMO_USERS = [
    {"username":"admin","email":"admin@lms.local","is_staff":True,"is_superuser":True,"is_instructor":True,"password":"password"},
    {"username":"inst_alice","email":"alice@lms.local","is_staff":True,"is_superuser":False,"is_instructor":True,"password":"password"},
    {"username":"student_bob","email":"bob@lms.local","is_staff":False,"is_superuser":False,"is_instructor":False,"password":"password"},
]

SAMPLE_SUB = b"Submission for assignment %d\nStudent: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for lms app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding lms demo...")
            users = self._create_users()
            instructors = [u for u in users if getattr(u, "is_instructor", False)]
            if not instructors: instructors = [users[0]] if users else []

            # create course, assignment, submissions
            course, _ = Course.objects.get_or_create(title="Demo Course")
            for inst in instructors:
                course.instructors.add(inst)
            assignment, _ = Assignment.objects.get_or_create(course=course, title="Demo Assignment")
            sub_users = [u for u in users if not getattr(u, "is_instructor", False)]
            created_subs = []
            for i, student in enumerate(sub_users, start=1):
                s = Submission(assignment=assignment, student=student)
                fname = f"{student.username}_sub_{i}.txt"
                s.filename = fname
                s.file.save(fname, ContentFile(SAMPLE_SUB % (assignment.id, student.username.encode())), save=True)
                created_subs.append(s)
                self.stdout.write(f"  + submission {s.file.name} by {student.username}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("LMS demo seeded."))

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
            if hasattr(u, "is_instructor") and getattr(u, "is_instructor") != cfg.get("is_instructor", False):
                setattr(u, "is_instructor", cfg.get("is_instructor", False)); changed = True
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
            f.write(b"LMS_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
