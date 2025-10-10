from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "lms"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("assignments/<int:assignment_id>/", views.assignment_view, name="assignment_view"),
    path("storage/submissions/<int:submission_id>/download/", views.download_submission_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="lms/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="lms:login"), name="logout"),

    # Instructor area
    path("instructor/assignments/", views.instructor_assignments, name="instructor_assignments"),
    path("submissions/<int:submission_id>/", views.submission_detail, name="list"),
    path("files/<int:submission_id>/download/", views.download_submission, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
