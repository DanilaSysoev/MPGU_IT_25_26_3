from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "real_estate"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("listings/<int:listing_id>/", views.listing_view, name="listing_view"),
    path("storage/docs/<int:doc_id>/download/", views.download_doc_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="real_estate/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="real_estate:login"), name="logout"),

    # Agent / owner area
    path("agent/listings/", views.listings_list, name="list"),
    path("agent/listings/<int:listing_id>/", views.listing_detail, name="list"),
    path("files/<int:doc_id>/download/", views.download_doc, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
