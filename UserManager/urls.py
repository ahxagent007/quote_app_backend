from django.urls import path
from .views import *
from .api import *

urlpatterns = [
    path('login/otp', LoginOTP.as_view(), name='login-otp'),
    path('login/otp/verification', LoginOTPVerification.as_view(), name='login-otp-verification'),
]
