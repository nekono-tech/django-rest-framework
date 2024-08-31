from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Video
from .serializers import VideoSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 50

class IndexView(APIView):
    def get(self, request):
        query = request.query_params.get('search', None)
        videos = Video.objects.all()

        if query:
            videos = videos.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(videos, request, view=self)
        serializer = VideoSerializer(paginated_videos, many=True)
        return paginator.get_paginated_response(serializer.data)
