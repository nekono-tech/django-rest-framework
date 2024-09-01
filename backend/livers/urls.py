from django.urls import path
from .views import IndexView, DetailView

urlpatterns = [
    path('', IndexView.as_view(), name='livers.index'),
    path('<str:liver_id>/', DetailView.as_view(), name='livers.detail'),
]
