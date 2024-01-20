from django.urls import path
from .views import *
from .api import *


urlpatterns = [
    path('verification/create', VerificationCreateAPI.as_view(), name='verification-create'),
    path('verification', VerificationAPI.as_view(), name='verification'),
    path('notice/list/<int:id>', ChatAPI.as_view(), name='notice-list'),
    path('notice/create/<int:id>', ChatAPI.as_view(), name='notice'),

]
