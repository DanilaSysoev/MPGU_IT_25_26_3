from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/grade/list/', views.grade_list, name='grade_list'),
    path('vuln/grade/', views.grade_detail_vuln, name='grade_detail_vuln'),
    path('secure/grade/<int:obj_id>/', views.grade_detail_secure, name='grade_detail_secure'),
    path('vuln/grade/path/<int:obj_id>/', views.grade_detail_vuln_path, name='grade_detail_vuln_path'),
    path('vuln/grade/update/<int:obj_id>/', views.grade_update_vuln, name='grade_update_vuln'),

    path('secure/assignment/list/', views.assignment_list, name='assignment_list'),
    path('vuln/assignment/', views.assignment_detail_vuln, name='assignment_detail_vuln'),
    path('secure/assignment/<int:obj_id>/', views.assignment_detail_secure, name='assignment_detail_secure'),
    path('vuln/assignment/path/<int:obj_id>/', views.assignment_detail_vuln_path, name='assignment_detail_vuln_path'),
    path('vuln/assignment/update/<int:obj_id>/', views.assignment_update_vuln, name='assignment_update_vuln'),
]
