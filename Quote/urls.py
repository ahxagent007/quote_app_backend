from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('', QuoteAPI.as_view(), name='quote'),
    path('list', QuoteListAPI.as_view(), name='quote-list'),
]
