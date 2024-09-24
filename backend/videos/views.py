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
        pattern = request.query_params.get('pattern', None)
        videos = Video.objects.all()

        if query:
            # 前後の空白をカット
            query = query.strip()

            # クエリに含まれるスペースで区切る(全角スペースも含む)
            query = query.replace('　', ' ')
            query = query.split(' ')

            if pattern:
                # フィルタクエリを初期化
                filter_queries = Q()

                # patterns の各値に対応するフィルタリングを実行
                for q in query:
                    # patterns=1 でタイトルに絞り込み
                    if '1' in pattern.split(','):
                        filter_queries |= Q(title__icontains=q)

                    # patterns=2 で概要に絞り込み
                    if '2' in pattern.split(','):
                        filter_queries |= Q(description__icontains=q)

                    # patterns=3 でライバー名に絞り込み
                    if '3' in pattern.split(','):
                        filter_queries |= Q(youtube__liver__name__icontains=q)

                # フィルタクエリがある場合のみ動画リストに適用
                if filter_queries:
                    videos = videos.filter(filter_queries)
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
