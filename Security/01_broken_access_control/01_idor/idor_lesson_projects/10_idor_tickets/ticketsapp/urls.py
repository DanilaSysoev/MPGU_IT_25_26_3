from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/ticket/list/', views.ticket_list, name='ticket_list'),
    path('vuln/ticket/', views.ticket_detail_vuln, name='ticket_detail_vuln'),
    path('secure/ticket/<int:obj_id>/', views.ticket_detail_secure, name='ticket_detail_secure'),
    path('vuln/ticket/path/<int:obj_id>/', views.ticket_detail_vuln_path, name='ticket_detail_vuln_path'),
    path('vuln/ticket/update/<int:obj_id>/', views.ticket_update_vuln, name='ticket_update_vuln'),

    path('secure/message/list/', views.message_list, name='message_list'),
    path('vuln/message/', views.message_detail_vuln, name='message_detail_vuln'),
    path('secure/message/<int:obj_id>/', views.message_detail_secure, name='message_detail_secure'),
    path('vuln/message/path/<int:obj_id>/', views.message_detail_vuln_path, name='message_detail_vuln_path'),
    path('vuln/message/update/<int:obj_id>/', views.message_update_vuln, name='message_update_vuln'),
]
