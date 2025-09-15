from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Ticket #{self.id} {getattr(self,'title','')}"


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    def __str__(self): return f"Message #{self.id} {getattr(self,'text','')}"
