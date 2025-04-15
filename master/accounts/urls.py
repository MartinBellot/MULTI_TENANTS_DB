from django.urls import path
from frontend import views as frontend_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('launch-server/', frontend_views.launch_new_server, name='launch_new_server'),
    path('dashboard/', frontend_views.dashboard, name='dashboard'),

]