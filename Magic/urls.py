from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('verification/create', VerificationCreateAPI.as_view(), name='verification-create'),
    path('verification', VerificationAPI.as_view(), name='verification'),
    path('chat/messages/<int:id>', ChatAPI.as_view(), name='chat-list'),
    path('chat/messages/quick/<int:id>/<int:last_chat_id>', ChatFastAPI.as_view(), name='chat-list-quick'),

    path('chat/create/<int:id>', ChatAPI.as_view(), name='chat'),
    path('chat/list', ChatListAPI.as_view(), name='chat-list'),
    path('chat/start', ChartStart.as_view(), name='chat-start')

]
