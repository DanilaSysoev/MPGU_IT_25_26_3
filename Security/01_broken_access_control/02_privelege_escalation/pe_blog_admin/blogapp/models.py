from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, default="user")  # user, moderator, admin
    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self):
        return f"Item #{self.id}: {self.title}"
