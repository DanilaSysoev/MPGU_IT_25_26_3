from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "saas"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("projects/<int:project_id>/", views.project_view, name="project_view"),
    path("storage/attachments/<int:att_id>/download/", views.download_attachment_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="saas/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="saas:login"), name="logout"),

    # Projects / tasks
    path("projects/", views.projects_list, name="list"),
    path("tasks/<int:task_id>/", views.task_detail, name="list"),
    path("files/<int:att_id>/download/", views.download_attachment, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
