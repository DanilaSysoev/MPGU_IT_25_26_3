from django.contrib import admin
from .models import Message, Ticket

admin.site.register(Ticket)
admin.site.register(Message)
