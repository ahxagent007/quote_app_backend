from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import ChatSerializer, VerficationSerializer
from .models import chat, verification
import hashlib
from django.db.models import Q


class VerificationAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        '''
        {
            "passcode":"000000"
        }
        '''
        if request.data['passcode'] == "123456":
            data = {
                'page': 'quote'
            }
            return Response(data, status=status.HTTP_200_OK)

        user_id = request.user.id

        try:
            verf = verification.objects.get(user=user_id)

            if verf.passcode == md5_hash(request.data['passcode']):
                # matched
                data = {
                    'page': 'magic'
                }
            else:
                data = {
                    'page': 'wrong_pass'
                }
        except:
            data = {
                'page': 'wrong_pass'
            }
        return Response(data, status=status.HTTP_200_OK)

class VerificationCreateAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        '''
        {
            "passcode":"000000"
        }
        '''

        user_id = request.user.id
        json_data = request.data
        json_data['user'] = user_id
        json_data['passcode'] = md5_hash(json_data['passcode'])

        serializer = VerficationSerializer(data=json_data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'msg': 'Created'
        }
        return Response(data, status=status.HTTP_200_OK)

class ChatAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, id):
        user_id = request.user.id

        chats = ChatSerializer(chat.objects.filter(Q(chat_room_id=id) & Q(Q(sender=user_id) | Q(receiver=user_id))), many=True).data

        return Response(chats, status=status.HTTP_200_OK)

    def post(self, request, id):
        '''
        {
            "message": "asdasdasdasd asd asd asd ",
            "receiver": 1
        }
        '''

        json_data = request.data
        json_data['sender'] = request.user.id
        json_data['chat_room_id'] = id

        serializer = ChatSerializer(data=json_data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)




def md5_hash(txt):
    return hashlib.md5(txt.encode()).hexdigest()