from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    published_at = models.DateTimeField()
    thumbnail_default_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_medium_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_standard_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_high_url = models.URLField(max_length=255, null=True, blank=True)
    thumbnail_maxres_url = models.URLField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.title
