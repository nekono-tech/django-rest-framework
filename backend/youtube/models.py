from django.db import models

from common.models import BaseModel
from livers.models import Liver


class Youtube(BaseModel):
    liver = models.ForeignKey(Liver, on_delete=models.CASCADE)
    channel_id = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.channel_id
