from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/project/list/', views.project_list, name='project_list'),
    path('vuln/project/', views.project_detail_vuln, name='project_detail_vuln'),
    path('secure/project/<int:obj_id>/', views.project_detail_secure, name='project_detail_secure'),
    path('vuln/project/path/<int:obj_id>/', views.project_detail_vuln_path, name='project_detail_vuln_path'),
    path('vuln/project/update/<int:obj_id>/', views.project_update_vuln, name='project_update_vuln'),

    path('secure/workitem/list/', views.workitem_list, name='workitem_list'),
    path('vuln/workitem/', views.workitem_detail_vuln, name='workitem_detail_vuln'),
    path('secure/workitem/<int:obj_id>/', views.workitem_detail_secure, name='workitem_detail_secure'),
    path('vuln/workitem/path/<int:obj_id>/', views.workitem_detail_vuln_path, name='workitem_detail_vuln_path'),
    path('vuln/workitem/update/<int:obj_id>/', views.workitem_update_vuln, name='workitem_update_vuln'),
]
