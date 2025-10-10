from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "supplu_chain"

urlpatterns = [
    path("old/admin/maintenance/", views.admin_maintenance, name="admin_maintenance"),
    path("staging/debug/", views.staging_debug, name="staging_debug"),
    path("crash/", views.crash, name="crash"),

    path("items/<int:item_id>/", views.item_view, name="item_view"),
    path("storage/shipments/<int:doc_id>/download/", views.download_shipment_doc_vuln, name="download_vuln"),
    path("api/users/<int:user_id>/export/", views.export_user_profile, name="export_user_profile"),
    path("download/", views.download_by_token, name="download_by_token"),

    path("", views.index, name="index"),
    path("login/", auth_views.LoginView.as_view(template_name="supply_chain/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="supply_chain:login"), name="logout"),

    # Supply manager area
    path("supply/items/", views.items_list, name="list"),
    path("supply/items/<int:item_id>/", views.item_detail, name="list"),
    path("files/<int:doc_id>/download/", views.download_shipment_doc, name="download"),

    # Admin
    path("ui/admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
