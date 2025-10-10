from django.contrib import admin
from .models import (User, DocFile, Listing)

admin.site.register(User)
admin.site.register(DocFile),
admin.site.register(Listing)
