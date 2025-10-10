from django.contrib import admin
from .models import (User, MedicalReport, Patient)

admin.site.register(User)
admin.site.register(MedicalReport),
admin.site.register(Patient)
