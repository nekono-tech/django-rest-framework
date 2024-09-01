import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from googleapiclient.discovery import build
from config import settings
from videos.models import Video
from youtube.models import Youtube
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    help = 'データベース内のすべてのYouTubeチャンネルから動画を取得して保存する'

    def handle(self, *args, **options):
        api_key = settings.YOUTUBE_API_KEY
        youtube_api = build('youtube', 'v3', developerKey=api_key)

        channels = Youtube.objects.all()

        for youtube in channels:
            try:
                channel_id = youtube.channel_id
                # 古い動画が残らないように削除する
                Video.objects.filter(youtube=youtube).delete()
                self.stdout.write(self.style.SUCCESS(f"All videos for channel ID {channel_id} have been deleted."))

                uploads_playlist_id = self.get_uploads_playlist_id(youtube_api, channel_id)
                self.retrieve_and_store_videos(youtube_api, uploads_playlist_id, youtube)
                self.stdout.write(self.style.SUCCESS(f"Updated videos for channel ID {channel_id}."))

            except ObjectDoesNotExist:
                self.stderr.write(self.style.ERROR(f"Error: Youtube model with channel ID '{channel_id}' does not exist."))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing channel ID '{channel_id}': {e}"))

    def get_uploads_playlist_id(self, youtube, channel_id):
        """
        指定されたチャンネルIDからアップロードプレイリストIDを取得する
        """
        response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    def retrieve_and_store_videos(self, youtube_api, playlist_id, youtube):
        """
        プレイリストから動画を取得しデータベースに保存する
        """
        next_page_token = None

        while True:
            videos, next_page_token = self._fetch_videos(youtube_api, playlist_id, next_page_token)

            for item in videos:
                self._save_video_item(item, youtube)

            # 次のページがない場合は終了
            if not next_page_token:
                break

    def _fetch_videos(self, youtube_api, playlist_id, page_token):
        """
        YouTube APIから動画を取得する
        """
        request = youtube_api.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        response = request.execute()

        return response.get('items', []), response.get('nextPageToken')

    def _save_video_item(self, item, youtube):
        """
        取得した動画情報をデータベースに保存する
        """
        snippet = item['snippet']
        video_id = snippet['resourceId']['videoId']
        published_at = self._parse_published_at(snippet['publishedAt'])

        Video.objects.create(
            video_id=video_id,
            title=snippet['title'],
            description=snippet['description'],
            published_at=published_at,
            thumbnail_default_url=snippet['thumbnails'].get('default', {}).get('url'),
            thumbnail_medium_url=snippet['thumbnails'].get('medium', {}).get('url'),
            thumbnail_standard_url=snippet['thumbnails'].get('standard', {}).get('url'),
            thumbnail_high_url=snippet['thumbnails'].get('high', {}).get('url'),
            thumbnail_maxres_url=snippet['thumbnails'].get('maxres', {}).get('url'),
            youtube=youtube
        )
        self.stdout.write(self.style.SUCCESS(f"Video with ID {video_id} has been saved"))

    def _parse_published_at(self, published_at):
        """
        published_at を解析し、適切なタイムゾーンに変換する

        published_at: 例) 2024-01-01T12:34:56Z
        """
        utc_time = datetime.datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        aware_utc_time = timezone.make_aware(utc_time, datetime.timezone.utc)
        return timezone.localtime(aware_utc_time)
