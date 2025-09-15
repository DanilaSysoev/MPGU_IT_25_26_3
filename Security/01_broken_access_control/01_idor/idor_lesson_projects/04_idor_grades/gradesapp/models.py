from django.db import models
from django.contrib.auth.models import User

class Grade(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Grade #{self.id} {getattr(self,'title','')}"


class Assignment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Assignment #{self.id} {getattr(self,'title','')}"
