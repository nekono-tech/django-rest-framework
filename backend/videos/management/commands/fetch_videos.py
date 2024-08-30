from django.core.management import BaseCommand
from googleapiclient.discovery import build

from config import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        api_key = settings.YOUTUBE_API_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)

        # チャンネルIDを取得する処理
        # request = youtube.channels().list(
        #     part='snippet,contentDetails',
        #     forHandle='@Dola'
        # )
        # response = request.execute()
        # if 'items' in response and len(response['items']) > 0:
        #     channel_id = response['items'][0]['id']
        # else:
        #     print("チャンネルが見つかりません。")
        #     return

        # 直接チャンネルIDを指定
        channel_id = 'UC53UDnhAAYwvNO7j_2Ju1cQ'

        # チャンネルのアップロードプレイリストIDを取得
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        # アップロードプレイリストIDを取得
        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # 動画ID、タイトル、作成日時をすべて取得するための初期設定
        next_page_token = None

        with open('video_data.txt', 'w', encoding='utf-8') as file:
            while True:
                # プレイリストIDを使って動画一覧を取得する
                playlist_request = youtube.playlistItems().list(
                    part='snippet',
                    playlistId=uploads_playlist_id,
                    maxResults=50,  # 一度に取得する最大数（50が上限）
                    pageToken=next_page_token
                )
                playlist_response = playlist_request.execute()

                for item in playlist_response.get('items', []):
                    video_id = item['snippet']['resourceId']['videoId']
                    title = item['snippet']['title']
                    published_at = item['snippet']['publishedAt']
                    if video_id:
                        file.write(f"{video_id}, {title}, {published_at}\n")

                file.write("============================\n")

                new_page_token = playlist_response.get('nextPageToken')
                if not new_page_token or new_page_token == next_page_token:
                    print("取得終了: 次のページがないか、ページトークンが変わっていません。")
                    break

                next_page_token = new_page_token

        print("全ての動画の取得が完了しました。")