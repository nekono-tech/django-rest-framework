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
        query = request.query_params.get('q', None)
        order = request.query_params.get('order', 'desc')
        livers = request.query_params.get('livers', None)
        videos = Video.objects.all()

        if query:
            # 前後の空白をカット
            query = query.strip()

            # クエリに含まれるスペースで区切る(全角スペースも含む)
            query = query.replace('　', ' ')
            query = query.split(' ')

            # クエリに含まれる単語を含む動画を取得
            for q in query:
                videos = videos.filter(
                    Q(title__icontains=q) | Q(description__icontains=q) | Q(youtube__liver__name__icontains=q)
                )

        if order == 'asc':
            videos = videos.order_by('published_at')
        else:
            videos = videos.order_by('-published_at')

        if livers:
            videos = videos.filter(youtube__liver__in=livers.split(','))

        paginator = CustomPageNumberPagination()
        paginated_videos = paginator.paginate_queryset(videos, request, view=self)
        serializer = VideoSerializer(paginated_videos, many=True)
        return paginator.get_paginated_response(serializer.data)


class DetailView(APIView):
    def get(self, request, video_id):
        video = Video.objects.get(video_id=video_id)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
