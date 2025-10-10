import os, uuid
from typing import Optional
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

def statement_upload_to(instance: "Statement", filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return f"statements/{instance.account.id}/{uuid.uuid4().hex}{ext}"


class User(AbstractUser):
    is_teller = models.BooleanField(default=False, help_text="HR сотрудник")
    is_admin = models.BooleanField(default=False, help_text="Администратор портала")

    def __str__(self) -> str:
        return self.get_username()
    
    def description(self, include_candidates: bool = True) -> str:
        """
        Возвращает человекочитаемую строку с информацией о пользователе.
        - include_candidates: если True и пользователь is_teller, добавляет краткую сводку по кандидатам.

        ВАЖНО: НЕ включать сюда пароли/хеши/секреты, если это не учебная локальная демо-ветка.
        Для учебной демонстрации можно показывать email, username и список кандидатов.
        """
        parts = []
        parts.append(f"User: id={self.pk}, username={self.get_username()}, email={self.email}")
        parts.append(f"roles: is_teller={getattr(self, 'is_teller', False)}, is_admin={getattr(self, 'is_admin', False)}")
        # опционально можно добавить дату последнего логина, если нужно:
        if hasattr(self, "last_login") and self.last_login:
            parts.append(f"last_login={self.last_login.isoformat()}")
        # Добавляем кандидатов, если это HR и разрешено
        if include_candidates and getattr(self, "is_teller", False):
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

class Account(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="accounts")
    number = models.CharField(max_length=64, unique=True)

    def __str__(self) -> str:
        return f"Acct {self.number}"

class Statement(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name="statements")
    file = models.FileField(upload_to=statement_upload_to)
    filename = models.CharField(max_length=512, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *a, **kw):
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*a, **kw)

    def __str__(self) -> str:
        return f"Statement {self.pk} for {self.account}"

    def is_accessible_by(self, user: Optional[settings.AUTH_USER_MODEL]) -> bool:
        if not user or not user.is_authenticated:
            return False
        # only account owner or bank staff/admin
        if user.is_staff or user.is_superuser:
            return True
        return user == self.account.owner
