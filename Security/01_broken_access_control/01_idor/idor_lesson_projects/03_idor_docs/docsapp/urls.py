from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/document/list/', views.document_list, name='document_list'),
    path('vuln/document/', views.document_detail_vuln, name='document_detail_vuln'),
    path('secure/document/<int:obj_id>/', views.document_detail_secure, name='document_detail_secure'),
    path('vuln/document/path/<int:obj_id>/', views.document_detail_vuln_path, name='document_detail_vuln_path'),
    path('vuln/document/update/<int:obj_id>/', views.document_update_vuln, name='document_update_vuln'),

    path('secure/fileentry/list/', views.fileentry_list, name='fileentry_list'),
    path('vuln/fileentry/', views.fileentry_detail_vuln, name='fileentry_detail_vuln'),
    path('secure/fileentry/<int:obj_id>/', views.fileentry_detail_secure, name='fileentry_detail_secure'),
    path('vuln/fileentry/path/<int:obj_id>/', views.fileentry_detail_vuln_path, name='fileentry_detail_vuln_path'),
    path('vuln/fileentry/update/<int:obj_id>/', views.fileentry_update_vuln, name='fileentry_update_vuln'),
]
