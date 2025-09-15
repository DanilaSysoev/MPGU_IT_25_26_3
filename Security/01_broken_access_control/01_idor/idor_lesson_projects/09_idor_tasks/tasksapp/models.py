from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Task #{self.id} {getattr(self,'title','')}"


class TaskComment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    def __str__(self): return f"TaskComment #{self.id} {getattr(self,'text','')}"
