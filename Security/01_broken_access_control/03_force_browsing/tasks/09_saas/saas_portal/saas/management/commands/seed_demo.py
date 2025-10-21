from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from django.conf import settings
import os

from saas.models import Project, Task, Attachment, User

DEMO_USERS = [
    {"username":"admin","email":"admin@pm.local","is_staff":True,"is_superuser":True,"is_project_manager":True,"password":"password"},
    {"username":"mgr_kate","email":"kate@pm.local","is_staff":True,"is_superuser":False,"is_project_manager":True,"password":"password"},
    {"username":"dev_dan","email":"dan@pm.local","is_staff":False,"is_superuser":False,"is_project_manager":False,"password":"password"},
]

SAMPLE_ATTACH = b"Attachment for task %s\nUploaded by: %s\n"

class Command(BaseCommand):
    help = "Seed demo data for pm app"

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write("Seeding pm demo...")
            users = self._create_users()
            managers = [u for u in users if getattr(u, "is_project_manager", False)]
            members = [u for u in users if not getattr(u, "is_project_manager", False)]

            project, _ = Project.objects.get_or_create(name="Demo Project")
            for m in managers + members:
                project.members.add(m)

            task, _ = Task.objects.get_or_create(project=project, title="Initial task")
            att = Attachment(task=task)
            fname = f"{task.id}_spec.txt"
            att.filename = fname
            att.file.save(fname, ContentFile(SAMPLE_ATTACH % (task.title.encode(), managers[0].username.encode() if managers else b"admin")), save=True)
            self.stdout.write(f"  + task attachment -> {att.file.name}")

            self._create_static_backup()
            self.stdout.write(self.style.SUCCESS("PM demo seeded."))

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
            if hasattr(u, "is_project_manager") and getattr(u, "is_project_manager") != cfg.get("is_project_manager", False):
                setattr(u, "is_project_manager", cfg.get("is_project_manager", False))
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
            f.write(b"PM_FAKE_SECRET=demo")
        self.stdout.write("  + created static/backups/.env.backup")
