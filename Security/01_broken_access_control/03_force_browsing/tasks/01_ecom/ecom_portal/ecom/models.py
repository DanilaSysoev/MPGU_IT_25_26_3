import os, uuid
from typing import Optional
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

def invoice_upload_to(instance: "InvoiceFile", filename: str) -> str:
    ext = os.path.splitext(filename)[1]
    return f"invoices/{instance.order.id}/{uuid.uuid4().hex}{ext}"


class User(AbstractUser):
    is_mgr = models.BooleanField(default=False, help_text="Менеджер")
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
        parts.append(f"roles: is_hr={getattr(self, 'is_mgr', False)}, is_admin={getattr(self, 'is_admin', False)}")
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


class Order(models.Model):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["customer"])]

    def __str__(self) -> str:
        return f"Order #{self.pk} ({self.customer})"

class InvoiceFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    file = models.FileField(upload_to=invoice_upload_to)
    filename = models.CharField(max_length=512, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]
        indexes = [models.Index(fields=["order"])]

    def __str__(self) -> str:
        return f"Invoice {self.pk} for order {self.order_id}"

    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = os.path.basename(self.file.name)
        super().save(*args, **kwargs)

    def is_accessible_by(self, user: Optional[settings.AUTH_USER_MODEL]) -> bool:
        if not user or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        return user == self.order.customer
