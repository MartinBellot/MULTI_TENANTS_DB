# server_creation/urls.py
from django.urls import path
from . import views

app_name = 'server_creation'

urlpatterns = [
    path('', views.server_list, name='server_list'),
    path('create/', views.server_create, name='server_create'),
    path('<int:pk>/stop/', views.server_stop, name='server_stop'),
    path('<int:pk>/start/', views.server_start, name='server_start'),
    path('<int:pk>/restart/', views.server_restart, name='server_restart'),
]