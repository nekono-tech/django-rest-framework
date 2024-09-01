from django.db import models

from common.models import BaseModel
from youtube.models import Youtube


class Video(BaseModel):
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_default_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_medium_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_standard_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_high_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_maxres_url = models.URLField(max_length=255, null=True, blank=True)

    youtube = models.ForeignKey(Youtube, related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'videos'
