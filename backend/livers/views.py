from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Liver
from .serializers import LiverSerializer


class IndexView(APIView):
    def get(self, request):
        livers = Liver.objects.all()
        serializer = LiverSerializer(livers, many=True)
        return Response(serializer.data)


class DetailView(APIView):
    def get(self, request, liver_id):
        liver = Liver.objects.get(id=liver_id)
        serializer = LiverSerializer(liver)
        return Response(serializer.data)
