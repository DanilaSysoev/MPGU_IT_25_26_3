from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/client/list/', views.client_list, name='client_list'),
    path('vuln/client/', views.client_detail_vuln, name='client_detail_vuln'),
    path('secure/client/<int:obj_id>/', views.client_detail_secure, name='client_detail_secure'),
    path('vuln/client/path/<int:obj_id>/', views.client_detail_vuln_path, name='client_detail_vuln_path'),
    path('vuln/client/update/<int:obj_id>/', views.client_update_vuln, name='client_update_vuln'),

    path('secure/deal/list/', views.deal_list, name='deal_list'),
    path('vuln/deal/', views.deal_detail_vuln, name='deal_detail_vuln'),
    path('secure/deal/<int:obj_id>/', views.deal_detail_secure, name='deal_detail_secure'),
    path('vuln/deal/path/<int:obj_id>/', views.deal_detail_vuln_path, name='deal_detail_vuln_path'),
    path('vuln/deal/update/<int:obj_id>/', views.deal_update_vuln, name='deal_update_vuln'),
]
