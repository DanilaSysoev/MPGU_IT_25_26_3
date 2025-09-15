from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self): return f"Product #{self.id} {getattr(self,'name','')}"


class Supply(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Supply #{self.id} {getattr(self,'title','')}"
