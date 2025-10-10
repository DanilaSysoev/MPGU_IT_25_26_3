import os, uuid
from typing import Optional
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

def report_upload_to(instance: "MedicalReport", filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return f"reports/{instance.patient.id}/{uuid.uuid4().hex}{ext}"

class User(AbstractUser):
    is_doctor = models.BooleanField(default=False, help_text="Доктор")
    is_admin = models.BooleanField(default=False, help_text="Администратор портала")

    def __str__(self) -> str:
        return self.get_username()
    
    def description(self, include_candidates: bool = True) -> str:
        """
        Возвращает человекочитаемую строку с информацией о пользователе.
        - include_candidates: если True и пользователь is_doctor, добавляет краткую сводку по кандидатам.

        ВАЖНО: НЕ включать сюда пароли/хеши/секреты, если это не учебная локальная демо-ветка.
        Для учебной демонстрации можно показывать email, username и список кандидатов.
        """
        parts = []
        parts.append(f"User: id={self.pk}, username={self.get_username()}, email={self.email}")
        parts.append(f"roles: is_doctor={getattr(self, 'is_doctor', False)}, is_admin={getattr(self, 'is_admin', False)}")
        # опционально можно добавить дату последнего логина, если нужно:
        if hasattr(self, "last_login") and self.last_login:
            parts.append(f"last_login={self.last_login.isoformat()}")
        # Добавляем кандидатов, если это HR и разрешено
        if include_candidates and getattr(self, "is_doctor", False):
            # выбираем минимальный набор данных — id и имя
            qs = getattr(self, "candidates", None)
            if qs is not None:
                cand_infos = []
                # ограничим вывод, чтобы не засорять сообщение (например, до 20)
                for c in qs.all()[:20]:
                    cand_infos.append(f"{c.id}:{c.full_name}")
                if cand_infos:
                    parts.append("candidates=[" + ", ".join(cand_infos) + (", ...]" if qs.count() > 20 else "]"))
                else:
                    parts.append("candidates=[]")
        return " | ".join(parts)

class Patient(models.Model):
    full_name = models.CharField(max_length=255)
    dob = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.full_name

class MedicalReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="reports")
    file = models.FileField(upload_to=report_upload_to)
    filename = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["patient"])]

    def __str__(self) -> str:
        return f"Report {self.pk} for {self.patient}"

    def save(self, *a, **kw):
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*a, **kw)

    def is_accessible_by(self, user: Optional[settings.AUTH_USER_MODEL]) -> bool:
        if not user or not user.is_authenticated:
            return False
        # doctors (is_doctor flag), patient creator, or admin/superuser
        if getattr(user, "is_doctor", False) or user.is_superuser:
            return True
        return user == self.patient.created_by
