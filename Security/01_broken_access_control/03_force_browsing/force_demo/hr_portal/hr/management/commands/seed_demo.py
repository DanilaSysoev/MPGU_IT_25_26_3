from typing import Optional

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction

from hr.models import Candidate, ResumeFile, User

DEMO_USERS = [
    {
        "username": "admin",
        "email": "admin@example.com",
        "is_staff": True,
        "is_superuser": True,
        "is_admin": True,
        "is_hr": True,
        "password": "password",
    },
    {
        "username": "hr_alice",
        "email": "alice.hr@example.com",
        "is_staff": True,
        "is_superuser": False,
        "is_admin": False,
        "is_hr": True,
        "password": "password",
    },
    {
        "username": "hr_bob",
        "email": "bob.hr@example.com",
        "is_staff": False,
        "is_superuser": False,
        "is_admin": False,
        "is_hr": True,
        "password": "password",
    },
    {
        "username": "user_charlie",
        "email": "charlie.user@example.com",
        "is_staff": False,
        "is_superuser": False,
        "is_admin": False,
        "is_hr": False,
        "password": "password",
    },
]

DEMO_CANDIDATES = [
    {"full_name": "Ivan Petrov", "email": "ivan.petrov@example.com", "phone": "+7-901-000-0001"},
    {"full_name": "Maria Ivanova", "email": "maria.ivanova@example.com", "phone": "+7-901-000-0002"},
    {"full_name": "John Smith", "email": "john.smith@example.com", "phone": "+1-555-0100"},
]

SAMPLE_RESUME_CONTENT = b"Sample resume content (demo).\nCandidate: %s\n"


class Command(BaseCommand):
    help = "Seeds demo users, candidates and resumes for the HRPortal training app."

    def handle(self, *args, **options):
        with transaction.atomic():
            self.stdout.write(self.style.NOTICE("Seeding demo data..."))
            users = self._create_users()
            hr_users = [u for u in users if getattr(u, "is_hr", False)]
            if not hr_users and users:
                hr_users = [users[0]]

            created_candidates = []
            created_resumes = []

            for i, c in enumerate(DEMO_CANDIDATES):
                owner = hr_users[i % len(hr_users)] if hr_users else None
                candidate = self._upsert_candidate(c, owner)
                created_candidates.append(candidate)

                # 1–2 резюме на кандидата
                for j in range(1, 3):
                    resume = self._create_resume(candidate, owner, j)
                    created_resumes.append(resume)

            self.stdout.write("")
            self.stdout.write(self.style.SUCCESS("=== RESULT ==="))
            for u in users:
                pwd = next((x["password"] for x in DEMO_USERS if x["username"] == u.username), "password")
                self.stdout.write(
                    f"User: {u.username}  "
                    f"(is_hr={getattr(u, 'is_hr', False)}, is_admin={getattr(u, 'is_admin', False)})  "
                    f"password: {pwd}"
                )
            self.stdout.write("Candidates: " + ", ".join(c.full_name for c in created_candidates))
            self.stdout.write("Resumes:")
            for r in created_resumes:
                self.stdout.write(f"  - #{r.id} {r.file.name} (candidate_id={r.candidate_id})")

            self.stdout.write(self.style.SUCCESS("\nDemo data seeded."))

    # ---------- helpers ----------

    def _create_users(self) -> list[User]:
        out: list[User] = []
        for cfg in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=cfg["username"],
                defaults={"email": cfg["email"]},
            )
            changed = False
            if created:
                user.set_password(cfg["password"])
                changed = True
            # базовые роли/флаги
            fields = ("is_staff", "is_superuser")
            for f in fields:
                if getattr(user, f) != cfg[f]:
                    setattr(user, f, cfg[f])
                    changed = True
            # кастомные поля из нашей модели
            for f in ("is_hr", "is_admin"):
                if hasattr(user, f) and getattr(user, f) != cfg[f]:
                    setattr(user, f, cfg[f])
                    changed = True
            if changed:
                user.save()
                self.stdout.write(self.style.SUCCESS(f"  + user {user.username} (created/updated)"))
            else:
                self.stdout.write(f"  = user {user.username} (unchanged)")
            out.append(user)
        return out

    def _upsert_candidate(self, data: dict, owner: Optional[User]) -> Candidate:
        cand, created = Candidate.objects.get_or_create(
            full_name=data["full_name"],
            defaults={
                "email": data["email"],
                "phone": data["phone"],
                "created_by": owner,
                "is_public": False,
            },
        )
        if not created:
            cand.email = data["email"]
            cand.phone = data["phone"]
            if owner:
                cand.created_by = owner
            cand.save(update_fields=["email", "phone", "created_by"])
            self.stdout.write(f"  = candidate {cand.id}: {cand.full_name} (updated)")
        else:
            self.stdout.write(self.style.SUCCESS(f"  + candidate {cand.id}: {cand.full_name} (owner={owner and owner.username})"))
        return cand

    def _create_resume(self, candidate: Candidate, owner: Optional[User], index: int) -> ResumeFile:
        fname = f"{candidate.full_name.replace(' ', '_')}_resume_{index}.txt"
        content = SAMPLE_RESUME_CONTENT % candidate.full_name.encode("utf-8")
        if owner:
            content += b"uploaded_by=" + owner.username.encode("utf-8") + b"\n"

        resume = ResumeFile(candidate=candidate, uploaded_by=owner)
        resume.file.save(fname, ContentFile(content), save=False)
        resume.filename = fname
        resume.save()
        self.stdout.write(f"    * resume #{resume.id} -> {resume.file.name}")
        return resume
