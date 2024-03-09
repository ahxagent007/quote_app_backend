from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .serializers import ChatSerializer, VerficationSerializer, LastSeenSerializer
from .models import chat, verification, last_seen
import hashlib
from django.db.models import Q
from UserManager.models import user
from UserManager.serializers import UserSerializer

from functions.common import current_milli_time, \
    format_convert_datetime_to_str



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

    def get(self, request, room_id):
        user_id = request.user.id


        chat_objs = chat.objects.filter(Q(chat_room_id=room_id) & Q(Q(sender=user_id) | Q(receiver=user_id)))

        try:
            first_chat = chat_objs.first()
            if not first_chat.sender == user_id:
                last_seen_id = first_chat.sender
            else:
                last_seen_id = first_chat.receiver
        except:
            last_seen_id = -1

        try:
            last_seen_obj = LastSeenSerializer(last_seen.objects.get(user = last_seen_id), many=False).data
            last_seen_str = format_convert_datetime_to_str(last_seen_obj['last_time'])
        except Exception as e:
            print(str(e))
            last_seen_str = 'Not Available'

        chats = ChatSerializer(chat_objs, many=True).data

        for c in chats:
            c['created_time'] = format_convert_datetime_to_str(c['created_time'])

        data = {
            'chats': chats,
            'last_seen': last_seen_str
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, room_id):
        '''
        {
            "message": "asdasdasdasd asd asd asd ",
            "receiver": 1
        }
        '''

        json_data = request.data
        json_data['sender'] = request.user.id
        json_data['chat_room_id'] = room_id

        serializer = ChatSerializer(data=json_data, many=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    def delete(self, request, room_id):
        chats_obj = chat.objects.filter(chat_room_id=room_id)
        chats_obj.delete()

        data = {
            'msg': 'Messages Deleted for both'
        }
        return Response(data, status=status.HTTP_200_OK)


class ChatFastAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request, room_id, last_chat_id):
        user_id = request.user.id
        chat_objs = chat.objects.filter(Q(chat_room_id=room_id) & Q(Q(sender=user_id) | Q(receiver=user_id)) & Q(id__gt=last_chat_id))
        chats = ChatSerializer(chat_objs, many=True).data

        try:
            first_chat = chat_objs.first()
            if not first_chat.sender == user_id:
                last_seen_id = first_chat.sender
            else:
                last_seen_id = first_chat.receiver
        except:
            last_seen_id = -1

        try:
            last_seen_obj = last_seen.objects.get(user=last_seen_id).last_time
            last_seen_str = format_convert_datetime_to_str(last_seen_obj)
        except Exception as e:
            print(str(e))
            last_seen_str = 'Not Available'

        chats = ChatSerializer(chat_objs, many=True).data

        for c in chats:
            c['created_time'] = format_convert_datetime_to_str(c['created_time'])

        data = {
            'chats': chats,
            'last_seen': last_seen_str
        }

        return Response(data, status=status.HTTP_200_OK)

class ChatListAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id

        chats_room_ids = chat.objects.filter(Q(sender=user_id) | Q(receiver=user_id)).values('chat_room_id').distinct()
        print(chats_room_ids)
        rooms = []

        for id in chats_room_ids:
            r = chat.objects.filter(chat_room_id=id['chat_room_id']).first()

            if not user_id == r.sender:
                chat_user = UserSerializer(user.objects.get(id=r.sender), many=False).data
            else:
                chat_user = UserSerializer(user.objects.get(id=r.receiver), many=False).data

            d = {
                'room_id': r.chat_room_id,
                'chat_user': chat_user,
            }
            rooms.append(d)

        data = {
            'chat_rooms': rooms
        }
        return Response(data, status=status.HTTP_200_OK)

def md5_hash(txt):
    return hashlib.md5(txt.encode()).hexdigest()

class ChartStart(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):

        '''
        {
            "email" : "asd@asd.com"
        }
        '''

        try:
            receiver = user.objects.get(email=request.data['email'])

        except Exception as e:
            data = {
                'msg': 'User Not Found',
                'error': str(e)
            }

            return Response(data, status=status.HTTP_200_OK)

        current_milis_str = str(current_milli_time())

        #start Chat
        chat.objects.create(message='Chat Started', sender=request.user.id,
                            receiver=receiver.id, chat_room_id=current_milis_str)

        data = {
            'msg': 'Success',
            'room_id': current_milis_str
        }

        return Response(data, status=status.HTTP_200_OK)

class DeleteChat(APIView):
    authentication_classes = [JWTAuthentication]

    def delete(self, request, room_id):

        user_id = request.user.id
        chat_user_ids = chat.objects.filter(Q(chat_room_id=room_id) & (Q(sender=user_id) | Q(receiver=user_id))).values('sender', 'receiver').distinct()

        chat_user_ids_uniq = []

        for ch in chat_user_ids:
            chat_user_ids_uniq.append(ch['sender'])
            chat_user_ids_uniq.append(ch['receiver'])

        chat_user_ids_uniq = list(set(chat_user_ids_uniq))

        data = {

        }
        if user_id in chat_user_ids_uniq:
            #delete
            chat.objects.filter(chat_room_id=room_id).delete()
            data['msg'] = 'Delete Completed'
        else:
            data['msg'] = 'Not Deleted'
        return Response(data, status=status.HTTP_200_OK)

class LastSeenAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user_id = request.user.id

        try:
            last_seen_obj = last_seen.objects.get(user=user_id)
            last_seen_obj.save()
            msg = 'Last Seen Updated'
        except Exception as e:
            msg = 'Last Seen Created'
            last_seen_obj = last_seen.objects.create(user=user_id)


        data = {
            'msg': msg,
            'last_seen_time': last_seen_obj.last_time
        }

        return Response(data, status=status.HTTP_200_OK)