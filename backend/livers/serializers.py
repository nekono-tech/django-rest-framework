from rest_framework import serializers

from livers.models import Liver


class LiverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liver
        fields = ('id', 'name')
