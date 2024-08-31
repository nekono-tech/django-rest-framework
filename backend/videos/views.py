from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Video
from .serializers import VideoSerializer


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 50

class IndexView(APIView):
    def get(self, request):
        query = request.query_params.get('search', None)
        order = request.query_params.get('order', 'desc')
        videos = Video.objects.all()

        if query:
            videos = videos.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )

        if order == 'asc':
            videos = videos.order_by('published_at')
        else:
            videos = videos.order_by('-published_at')

        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(videos, request, view=self)
        serializer = VideoSerializer(paginated_videos, many=True)
        return paginator.get_paginated_response(serializer.data)


class DetailView(APIView):
    def get(self, request, video_id):
        video = Video.objects.get(video_id=video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
