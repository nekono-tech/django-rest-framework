from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView


class ExampleView(APIView):
    def get(self, request):
        return Response(
            data={'message': 'get request'},
            status=HTTP_200_OK
        )

    def post(self, request):
        data = request.data
        return Response(
            data=data,
            status=HTTP_200_OK
        )
