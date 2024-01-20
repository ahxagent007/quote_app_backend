from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializer import QuoteSerializer
from .models import quote

class QuoteListAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        quotes = QuoteSerializer(quote.objects.all(), many=True).data

        data = {
            'quotes': quotes
        }

        return Response(data, status=status.HTTP_200_OK)

class QuoteAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        '''
        {
            "quote": "asd asd asd asd asdas dasd asd",
            "by": "xian"
        }
        '''
        json_data = request.data

        serializer = QuoteSerializer(data=json_data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)
