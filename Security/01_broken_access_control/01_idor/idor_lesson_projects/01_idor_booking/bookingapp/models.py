from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Booking #{self.id} {getattr(self,'title','')}"


class Payment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Payment #{self.id} {getattr(self,'title','')}"
