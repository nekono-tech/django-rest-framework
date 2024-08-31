from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('example/', include('example.urls')),
        path('videos/', include('videos.urls')),
    ]))
]
