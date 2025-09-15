from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/product/list/', views.product_list, name='product_list'),
    path('vuln/product/', views.product_detail_vuln, name='product_detail_vuln'),
    path('secure/product/<int:obj_id>/', views.product_detail_secure, name='product_detail_secure'),
    path('vuln/product/path/<int:obj_id>/', views.product_detail_vuln_path, name='product_detail_vuln_path'),
    path('vuln/product/update/<int:obj_id>/', views.product_update_vuln, name='product_update_vuln'),

    path('secure/supply/list/', views.supply_list, name='supply_list'),
    path('vuln/supply/', views.supply_detail_vuln, name='supply_detail_vuln'),
    path('secure/supply/<int:obj_id>/', views.supply_detail_secure, name='supply_detail_secure'),
    path('vuln/supply/path/<int:obj_id>/', views.supply_detail_vuln_path, name='supply_detail_vuln_path'),
    path('vuln/supply/update/<int:obj_id>/', views.supply_update_vuln, name='supply_update_vuln'),
]
