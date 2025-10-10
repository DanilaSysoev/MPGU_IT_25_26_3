from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "ecom"

urlpatterns = [
    # demo-vuln endpoints (do not enable in prod)
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    # vuln API / downloads
    path("orders/<int:order_id>/view/", views.order_view, name="order_view"),
    path("storage/invoices/<int:invoice_id>/download/", views.download_invoice_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    # index + auth
    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="ecom/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="ecom:login"), name="logout"),

    # Manager / ecom UI (protected)
    path("ecom/orders/", views.shop_orders_list, name="list"),
    path("ecom/orders/<int:order_id>/", views.shop_order_detail, name="detail"),
    path("files/<int:invoice_id>/download/", views.download_invoice_protected, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
