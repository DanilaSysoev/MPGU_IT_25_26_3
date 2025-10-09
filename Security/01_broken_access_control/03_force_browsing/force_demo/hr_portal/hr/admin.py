from django.contrib import admin
from .models import (User, Candidate, ResumeFile)

admin.site.register(User)
admin.site.register(Candidate),
admin.site.register(ResumeFile)
