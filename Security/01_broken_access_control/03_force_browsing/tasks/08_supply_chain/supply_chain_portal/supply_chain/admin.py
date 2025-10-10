from django.contrib import admin
from .models import (User, InventoryItem, ShipmentDocument, Supplier)

admin.site.register(User)
admin.site.register(InventoryItem),
admin.site.register(ShipmentDocument),
admin.site.register(Supplier)
