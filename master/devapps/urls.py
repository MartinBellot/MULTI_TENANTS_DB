# devapps/urls.py
from django.urls import path
from .views import ApplicationCreateView, ApplicationListView

app_name = 'devapps'

urlpatterns = [
    path('register/', ApplicationCreateView.as_view(), name='register'),
    path('list/', ApplicationListView.as_view(), name='application_list'),
]