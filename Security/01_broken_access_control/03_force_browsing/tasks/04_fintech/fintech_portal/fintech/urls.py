from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "fintech"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("accounts/<int:account_id>/", views.account_view, name="account_view"),
    path("storage/statements/<int:statement_id>/download/", views.download_statement_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="fintech/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="fintech:login"), name="logout"),

    # Teller area
    path("teller/accounts/", views.accounts_list, name="list"),
    path("teller/accounts/<int:account_id>/", views.account_detail, name="list"),
    path("files/<int:statement_id>/download/", views.download_statement, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
