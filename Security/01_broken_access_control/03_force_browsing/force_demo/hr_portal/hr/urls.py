from django.urls import path

from hr import views
from django.contrib.auth import views as auth_views

app_name = "hr"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),
    path("candidates/<int:candidate_id>/", views.candidate_view, name="candidate_view"),
    path("storage/files/<int:resume_id>/download/", views.download_resume, name="download_resume"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),
    
    path("", views.index, name="index"),
    
    path("login/", auth_views.LoginView.as_view(template_name="hr/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="hr:login"), name="logout"),

    # HR
    path("hr/candidates/", views.hr_candidates_list, name="hr_candidates_list"),
    path("hr/candidates/<int:candidate_id>/", views.hr_candidate_detail, name="hr_candidate_detail"),
    path("files/<int:resume_id>/download/", views.download_resume_protected, name="download_resume"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
