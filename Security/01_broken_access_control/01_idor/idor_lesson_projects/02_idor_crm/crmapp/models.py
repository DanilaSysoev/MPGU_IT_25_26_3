from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self): return f"Client #{self.id} {getattr(self,'name','')}"


class Deal(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Deal #{self.id} {getattr(self,'title','')}"
