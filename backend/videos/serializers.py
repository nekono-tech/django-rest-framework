from rest_framework import serializers

from videos.models import Video


class VideoSerializer(serializers.ModelSerializer):
    published_at = serializers.DateTimeField(format="%Y/%m/%d %H:%M")
    liver_name = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = [
            'video_id',
            'title',
            'description',
            'published_at',
            'thumbnail_default_url',
            'thumbnail_medium_url',
            'thumbnail_standard_url',
            'thumbnail_high_url',
            'liver_name',
        ]

    def get_liver_name(self, obj):
        return obj.youtube.liver.name if obj.youtube and obj.youtube.liver else None
