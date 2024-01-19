from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('/login/email', LoginOTP.as_view(), name='clinic-book-appointment'),
]
