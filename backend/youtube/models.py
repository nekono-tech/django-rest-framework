from django.db import models
from common.models import BaseModel
from livers.models import Liver


class Youtube(BaseModel):
    liver = models.ForeignKey(Liver, related_name='youtubes', on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=100)
    handle_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.channel_id

    class Meta:
        db_table = 'youtube'
