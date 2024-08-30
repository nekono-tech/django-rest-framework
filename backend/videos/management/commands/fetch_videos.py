from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from config import settings


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--id',
            type=str,
            required=True,
            help='YouTubeのチャンネルID（例: UCXXXXXXXXXXXX）'
        )

        parser.add_argument(
            '--num',
            type=int,
            required=False,
            help='取得処理の反復回数（例: 50）'
        )

    def handle(self, *args, **options):
        api_key = settings.YOUTUBE_API_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)

        channel_id = options['id']
        loop_num = options.get('num')

        uploads_playlist_id = self.get_uploads_playlist_id(youtube, channel_id)
        self.fetch_and_write_videos(youtube, uploads_playlist_id, loop_num)

        print("全ての動画の取得が完了しました。")

    def get_uploads_playlist_id(self, youtube, channel_id):
        """
        指定されたチャンネルIDからアップロードプレイリストIDを取得する
        """
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        # アップロードプレイリストIDを取得
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id

    def fetch_and_write_videos(self, youtube, uploads_playlist_id, loop_num):
        """
        プレイリストIDを使って動画を取得し、ファイルに書き込む
        """
        next_page_token = None

        with open('video_data.txt', 'w', encoding='utf-8') as file:
            if loop_num:
                for _ in range(loop_num):
                    next_page_token = self.fetch_videos(youtube, uploads_playlist_id, next_page_token, file)
                    if not next_page_token:
                        break
            else:
                while True:
                    next_page_token = self.fetch_videos(youtube, uploads_playlist_id, next_page_token, file)
                    if not next_page_token:
                        break

    def fetch_videos(self, youtube, playlist_id, page_token, file):
        """
        動画を取得し、次のページトークンを返す
        """
        playlist_request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=page_token
        )
        playlist_response = playlist_request.execute()

        for item in playlist_response.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            published_at = item['snippet']['publishedAt']
            if video_id:
                file.write(f"{video_id}, {title}, {published_at}\n")

        new_page_token = playlist_response.get('nextPageToken')
        if not new_page_token or new_page_token == page_token:
            return None

        return new_page_token
