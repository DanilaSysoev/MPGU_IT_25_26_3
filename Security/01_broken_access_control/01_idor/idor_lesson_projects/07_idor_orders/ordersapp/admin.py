from django.contrib import admin
from .models import Invoice, Order

admin.site.register(Order)
admin.site.register(Invoice)
