from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/task/list/', views.task_list, name='task_list'),
    path('vuln/task/', views.task_detail_vuln, name='task_detail_vuln'),
    path('secure/task/<int:obj_id>/', views.task_detail_secure, name='task_detail_secure'),
    path('vuln/task/path/<int:obj_id>/', views.task_detail_vuln_path, name='task_detail_vuln_path'),
    path('vuln/task/update/<int:obj_id>/', views.task_update_vuln, name='task_update_vuln'),

    path('secure/taskcomment/list/', views.taskcomment_list, name='taskcomment_list'),
    path('vuln/taskcomment/', views.taskcomment_detail_vuln, name='taskcomment_detail_vuln'),
    path('secure/taskcomment/<int:obj_id>/', views.taskcomment_detail_secure, name='taskcomment_detail_secure'),
    path('vuln/taskcomment/path/<int:obj_id>/', views.taskcomment_detail_vuln_path, name='taskcomment_detail_vuln_path'),
    path('vuln/taskcomment/update/<int:obj_id>/', views.taskcomment_update_vuln, name='taskcomment_update_vuln'),
]
