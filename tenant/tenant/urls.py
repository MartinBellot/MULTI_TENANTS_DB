from django.contrib import admin
from django.urls import path, include
from frontend.views import login_view
from django.conf import settings
from django.conf.urls.static import static
    

urlpatterns = [
    path('admin/', admin.site.urls),
    path('testapp/', include('testapp.urls')),
    path('login/', login_view, name='login'),
    path('files/', include('files.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
