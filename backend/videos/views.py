from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Video
from .serializers import VideoSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 50

class IndexView(APIView):
    def get(self, request):
        videos = Video.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(videos, request, view=self)
        serializer = VideoSerializer(paginated_videos, many=True)
        return paginator.get_paginated_response(serializer.data)
