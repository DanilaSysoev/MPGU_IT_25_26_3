from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/booking/list/', views.booking_list, name='booking_list'),
    path('vuln/booking/', views.booking_detail_vuln, name='booking_detail_vuln'),
    path('secure/booking/<int:obj_id>/', views.booking_detail_secure, name='booking_detail_secure'),
    path('vuln/booking/path/<int:obj_id>/', views.booking_detail_vuln_path, name='booking_detail_vuln_path'),
    path('vuln/booking/update/<int:obj_id>/', views.booking_update_vuln, name='booking_update_vuln'),

    path('secure/payment/list/', views.payment_list, name='payment_list'),
    path('vuln/payment/', views.payment_detail_vuln, name='payment_detail_vuln'),
    path('secure/payment/<int:obj_id>/', views.payment_detail_secure, name='payment_detail_secure'),
    path('vuln/payment/path/<int:obj_id>/', views.payment_detail_vuln_path, name='payment_detail_vuln_path'),
    path('vuln/payment/update/<int:obj_id>/', views.payment_update_vuln, name='payment_update_vuln'),
]
