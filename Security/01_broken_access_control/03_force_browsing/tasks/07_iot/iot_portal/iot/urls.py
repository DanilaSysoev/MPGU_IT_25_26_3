from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "iot"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("devices/<int:device_id>/", views.device_view, name="device_view"),
    path("storage/logs/<int:log_id>/download/", views.download_log_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="iot/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="iot:login"), name="logout"),

    # Device owner / tech
    path("devices/", views.devices_list, name="list"),
    path("devices/<int:device_id>/detail/", views.device_detail, name="list"),
    path("files/<int:log_id>/download/", views.download_log, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
