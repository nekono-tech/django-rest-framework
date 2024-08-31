from django.urls import path
from .views import IndexView, DetailView

urlpatterns = [
    path('', IndexView.as_view(), name='videos.index'),
    path('<str:video_id>/', DetailView.as_view(), name='videos.detail'),
]
