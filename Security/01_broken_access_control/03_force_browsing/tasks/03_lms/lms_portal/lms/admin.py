from django.contrib import admin
from .models import (User, Assignment, Course, Submission)

admin.site.register(User)
admin.site.register(Assignment),
admin.site.register(Course),
admin.site.register(Submission)
