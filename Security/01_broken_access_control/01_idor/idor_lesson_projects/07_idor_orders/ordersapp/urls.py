from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/order/list/', views.order_list, name='order_list'),
    path('vuln/order/', views.order_detail_vuln, name='order_detail_vuln'),
    path('secure/order/<int:obj_id>/', views.order_detail_secure, name='order_detail_secure'),
    path('vuln/order/path/<int:obj_id>/', views.order_detail_vuln_path, name='order_detail_vuln_path'),
    path('vuln/order/update/<int:obj_id>/', views.order_update_vuln, name='order_update_vuln'),

    path('secure/invoice/list/', views.invoice_list, name='invoice_list'),
    path('vuln/invoice/', views.invoice_detail_vuln, name='invoice_detail_vuln'),
    path('secure/invoice/<int:obj_id>/', views.invoice_detail_secure, name='invoice_detail_secure'),
    path('vuln/invoice/path/<int:obj_id>/', views.invoice_detail_vuln_path, name='invoice_detail_vuln_path'),
    path('vuln/invoice/update/<int:obj_id>/', views.invoice_update_vuln, name='invoice_update_vuln'),
]
