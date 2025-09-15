from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    def __str__(self): return f"Document #{self.id} {getattr(self,'title','')}"


class FileEntry(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self): return f"FileEntry #{self.id} {getattr(self,'name','')}"
