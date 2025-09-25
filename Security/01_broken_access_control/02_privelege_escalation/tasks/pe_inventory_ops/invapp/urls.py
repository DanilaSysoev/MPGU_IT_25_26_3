from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/items/', views.items_list, name='items_list'),

    path('vuln/delete_user/<int:user_id>/', views.delete_user_vuln, name='delete_user_vuln'),
    path('secure/delete_user/<int:user_id>/', views.delete_user_secure, name='delete_user_secure'),

    path('vuln/admin_panel/', views.admin_panel_vuln, name='admin_panel_vuln'),
    path('secure/admin_panel/', views.admin_panel_secure, name='admin_panel_secure'),

    path('vuln/promote_user/<int:user_id>/', views.promote_user_vuln, name='promote_user_vuln'),
    path('secure/promote_user/<int:user_id>/', views.promote_user_secure, name='promote_user_secure'),
]
