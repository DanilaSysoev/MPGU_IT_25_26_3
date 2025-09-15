from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Order #{self.id} {getattr(self,'title','')}"


class Invoice(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Invoice #{self.id} {getattr(self,'title','')}"
