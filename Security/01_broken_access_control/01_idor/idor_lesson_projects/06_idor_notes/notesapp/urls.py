from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('secure/note/list/', views.note_list, name='note_list'),
    path('vuln/note/', views.note_detail_vuln, name='note_detail_vuln'),
    path('secure/note/<int:obj_id>/', views.note_detail_secure, name='note_detail_secure'),
    path('vuln/note/path/<int:obj_id>/', views.note_detail_vuln_path, name='note_detail_vuln_path'),
    path('vuln/note/update/<int:obj_id>/', views.note_update_vuln, name='note_update_vuln'),

    path('secure/category/list/', views.category_list, name='category_list'),
    path('vuln/category/', views.category_detail_vuln, name='category_detail_vuln'),
    path('secure/category/<int:obj_id>/', views.category_detail_secure, name='category_detail_secure'),
    path('vuln/category/path/<int:obj_id>/', views.category_detail_vuln_path, name='category_detail_vuln_path'),
    path('vuln/category/update/<int:obj_id>/', views.category_update_vuln, name='category_update_vuln'),
]
