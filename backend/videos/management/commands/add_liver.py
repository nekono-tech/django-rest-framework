from django.core.management.base import BaseCommand
from googleapiclient.discovery import build
from config import settings
from livers.models import Liver
from youtube.models import Youtube


class Command(BaseCommand):
    help = '指定されたライバー情報を追加する'

    def add_arguments(self, parser):
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='ライバー名'
        )

        parser.add_argument(
            '--channel_id',
            type=str,
            required=True,
            help='チャンネルID'
        )

        parser.add_argument(
            '--handle',
            type=str,
            required=False,
            help='ハンドルネーム'
        )

    def handle(self, *args, **options):
        name = options['name']
        channel_id = options['channel_id']
        handle = options['handle'] or ''

        if Liver.objects.filter(name=name).exists():
            self.stderr.write(self.style.ERROR(f'Error: 同名のライバー "{name}" はすでに存在します'))
            return

        if Youtube.objects.filter(channel_id=channel_id).exists():
            self.stderr.write(self.style.ERROR(f'Error: 同じYouTube ID "{channel_id}" はすでに存在します'))
            return

        liver = Liver.objects.create(
            name=name,
        )
        liver.save()
        self.stdout.write(self.style.SUCCESS(f'Liver: {liver.name} を追加しました'))

        youtube = Youtube.objects.create(
            liver=liver,
            channel_id=channel_id,
            handle_name=handle,
        )
        youtube.save()
        self.stdout.write(self.style.SUCCESS(f'Youtube: {youtube.channel_id} を追加しました'))
