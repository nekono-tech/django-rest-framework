from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from config import settings


class Command(BaseCommand):
    help = 'YouTubeのハンドルネームからチャンネルIDを取得する'

    def add_arguments(self, parser):
        parser.add_argument(
            '--handle',
            type=str,
            required=True,
            help='YouTubeのハンドルネーム（例: @Example）'
        )

    def handle(self, *args, **options):
        api_key = settings.YOUTUBE_API_KEY
        youtube = build('youtube', 'v3', developerKey=api_key)

        handle = options['handle']
        request = youtube.channels().list(
            part='snippet',
            forHandle=handle # https://developers.google.com/youtube/v3/docs/channels/list?hl=ja&apix_params=%7B%22part%22%3A%5B%22snippet%2CcontentDetails%2Cstatistics%22%5D%2C%22forHandle%22%3A%22Dola%22%7D#parameters
        )

        response = request.execute()
        channel_id = ''
        if 'items' in response and len(response['items']) > 0:
            channel_id = response['items'][0]['id']
            return channel_id
        else:
            print("Not found channel id.")
            return channel_id
