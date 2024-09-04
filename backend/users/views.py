from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import CustomUser
from users.serializers import UserSerializer


class IndexView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DetailView(APIView):
    def get(self, request, user_id):
        print("user_id", user_id)
        user = CustomUser.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
