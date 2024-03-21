from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('verification/create', VerificationCreateAPI.as_view(), name='verification-create'),
    path('verification', VerificationAPI.as_view(), name='verification'),
    path('chat/messages/<str:room_id>', ChatAPI.as_view(), name='chat-list'),
    path('chat/messages/quick/<str:room_id>/<int:last_chat_id>', ChatFastAPI.as_view(), name='chat-list-quick'),

    path('chat/create/<str:room_id>', ChatAPI.as_view(), name='chat'),
    path('chat/list', ChatListAPI.as_view(), name='chat-list'),
    path('chat/start', ChartStart.as_view(), name='chat-start'),
    path('chat/delete/<str:room_id>', DeleteChat.as_view(), name='chat-delete'),
    path('chat/last_seen', LastSeenAPI.as_view(), name='chat-last-seen'),
    path('chat/image', ChatImageAPI.as_view(), name='chat-image'),
    path('app/report', AppReport.as_view(), name='app-report'),

]
