from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.file_upload, name='file_upload'),
    path('search/', views.file_search, name='file_search'),
    path('download/<int:pk>/', views.file_download, name='file_download'),
    path('delete/<int:pk>/', views.file_delete, name='file_delete'),
]