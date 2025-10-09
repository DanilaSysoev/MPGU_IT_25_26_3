import uuid
import os
from typing import Optional

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def resume_upload_to(instance: "ResumeFile", filename: str) -> str:
    """
    Путь загрузки резюме.
    В учебной vuln-версии можно сделать предсказуемые имена:
        f"resumes/{instance.candidate.id}/{filename}"
    В fixed-версии — использовать UUID для повышения безопасности.
    """
    # ext = os.path.splitext(filename)[1]
    # unique = uuid.uuid4().hex
    # return f"resumes/{instance.candidate.id}/{unique}{ext}"
    return f"resumes/{instance.candidate.id}/{filename}"


class User(AbstractUser):
    """
    Расширенная модель пользователя:
    - is_hr: пользователь — сотрудник HR (может создавать кандидатов)
    - is_admin: администратор портала
    """
    is_hr = models.BooleanField(default=False, help_text="HR сотрудник")
    is_admin = models.BooleanField(default=False, help_text="Администратор портала")

    def __str__(self) -> str:
        return self.get_username()
    
    def description(self, include_candidates: bool = True) -> str:
        """
        Возвращает человекочитаемую строку с информацией о пользователе.
        - include_candidates: если True и пользователь is_hr, добавляет краткую сводку по кандидатам.

        ВАЖНО: НЕ включать сюда пароли/хеши/секреты, если это не учебная локальная демо-ветка.
        Для учебной демонстрации можно показывать email, username и список кандидатов.
        """
        parts = []
        parts.append(f"User: id={self.pk}, username={self.get_username()}, email={self.email}")
        parts.append(f"roles: is_hr={getattr(self, 'is_hr', False)}, is_admin={getattr(self, 'is_admin', False)}")
        # опционально можно добавить дату последнего логина, если нужно:
        if hasattr(self, "last_login") and self.last_login:
            parts.append(f"last_login={self.last_login.isoformat()}")
        # Добавляем кандидатов, если это HR и разрешено
        if include_candidates and getattr(self, "is_hr", False):
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
        


class Candidate(models.Model):
    """
    Сущность кандидата, созданная HR-сотрудником.
    Демонстрация:
      - отсутствие проверки created_by → IDOR / force-browsing
    """
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=60, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="candidates",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False, help_text="Публичный профиль (для демонстрации)")

    class Meta:
        ordering = ["-date_created"]
        indexes = [
            models.Index(fields=["created_by"]),
            models.Index(fields=["email"]),
        ]

    def __str__(self) -> str:
        return self.full_name


class ResumeFile(models.Model):
    """
    Файлы с резюме, привязанные к кандидатам.
    Используются для демонстрации force-browsing:
    - /files/<id>/download без проверки прав → уязвимость.
    """
    candidate = models.ForeignKey(
        Candidate, on_delete=models.CASCADE, related_name="resumes"
    )
    file = models.FileField(upload_to=resume_upload_to)
    filename = models.CharField(max_length=512, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["candidate"]),
            models.Index(fields=["uploaded_at"]),
        ]

    def __str__(self) -> str:
        return f"Resume {self.pk} for {self.candidate.full_name}"

    def save(self, *args, **kwargs):
        # сохраняем оригинальное имя файла для информативности
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def owner(self) -> Optional[User]:
        """Владелец файла — HR, создавший кандидата."""
        return self.candidate.created_by

    def is_accessible_by(self, user: Optional[User]) -> bool:
        """
        Проверка прав доступа (для fixed-версии):
        доступ разрешён, если:
        - пользователь — админ
        - пользователь — владелец (создал кандидата)
        - пользователь — HR (по политике организации)
        """
        if user is None or not user.is_authenticated:
            return False
        if user.is_admin:
            return True
        if user == self.owner():
            return True
        if getattr(user, "is_hr", False):
            return True
        return False
