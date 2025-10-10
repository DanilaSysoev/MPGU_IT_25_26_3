from django.contrib import admin
from .models import (User, Case, CaseDocument)

admin.site.register(User)
admin.site.register(Case),
admin.site.register(CaseDocument)
