from django.contrib import admin
from .models import (User, Attachment, Project, Task)

admin.site.register(User)
admin.site.register(Attachment),
admin.site.register(Project),
admin.site.register(Task)
