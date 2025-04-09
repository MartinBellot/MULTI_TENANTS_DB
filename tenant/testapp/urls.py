# tenant_project/urls.py

from .views import protected_view
from django.urls import path

urlpatterns = [
    path('test/', protected_view, name='protected_view'),
]