from django.db import models

from common.models import BaseModel


class Liver(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'livers'
