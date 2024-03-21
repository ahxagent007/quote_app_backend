import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .email import send_mail
from .models import *
import random
import datetime
import pytz
from .serializers import UserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# class RegistrationAPI(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsCustomer]
#
#     @transaction.atomic
#     def post(self, request):
#         '''
#         {
#             "id": 1,
#             "name" : "XIAN",
#             "information" :
#                 {
#                     "gender" : "Male",
#                     "dob" : "2020-12-30",
#                     "location" : "Dhaka"
#                 },
#             "pets" : [
#                 {
#                     "name": "cutie",
#                     "gender" : "Male",
#                     "dob" : "2020-12-30",
#                     "type" : "Dog",
#                     "breed" : "German Shepard"
#                 },
#                 {
#                     "name": "cutie",
#                     "gender" : "Female",
#                     "dob" : "2020-12-30",
#                     "type" : "Dog",
#                     "breed" : "German Shepard"
#                 }
#             ]
#         }
#         '''
#
#         json_data = request.data
#
#         try:
#             user = User.objects.get(id=json_data['id'])
#
#             if not user.name == '':
#                 return Response({'msg': 'user already registered'}, status=status.HTTP_208_ALREADY_REPORTED)
#
#         except:
#             return Response({'msg':'User not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         user.name = json_data['name']
#         user.set_password(user.phone)
#
#         information = Information.objects.create(gender=json_data['information']['gender'], dob=json_data['information']['dob'], location=json_data['information']['location'])
#
#         user.information = information
#         pet_list = []
#         for pet_data in json_data['pets']:
#             pet = Pet.objects.create(gender=pet_data['gender'],dob=pet_data['dob'], type=pet_data['type'],
#                                      breed=pet_data['breed'], name=pet_data['name'])
#             user.pets.add(pet)
#             pet_list.append(pet)
#
#         user.save()
#
#         data = UserSerializer(user, many=False).data
#         refresh = RefreshToken.for_user(user)
#
#         data['refresh'] = str(refresh),
#         data['access'] = str(refresh.access_token),
#
#         return Response(data, status=status.HTTP_200_OK)


class LoginOTP(APIView):

    def post(self, request):
        '''
        {
            "email": "ahx.agent007@gmail.com"
        }
        '''

        email = request.data['email']

        rand_otp = random.randint(100000, 999999)

        try:
            otp_obj = otp.objects.get(email=email)
            otp_obj.otp = rand_otp
            otp_obj.created_date = datetime.datetime.now(pytz.timezone('Asia/Dhaka'))
            otp_obj.save()

            data = {
                'msg': 'OTP updated for {0}'.format(email)
            }
        except:
            otp.objects.create(email=email, otp=rand_otp)

            data = {
                'msg': 'OTP created for {0}'.format(email)
            }

        message = 'Your Quote App OTP is {0}'.format(rand_otp)
        send_mail(message, email)

        return Response(data, status=status.HTTP_200_OK)

class LoginOTPVerification(APIView):

    def post(self, request):
        '''
        {
            "email": "ahx.agent007@gmail.com",
            "otp": "123456",
            "phone": "One PLus"
        }
        '''

        email = request.data['email']
        user_otp = request.data['otp']
        phone = request.data['phone']

        errors = []
        try:
            otp_obj = otp.objects.get(email=email)
            if otp_obj.otp == user_otp:

                #login success
                try:
                    user_obj = user.objects.get(email=email)

                    if not user_obj.phone_model == phone:
                        message = "You have changed you mobile device for Quote App, if this login isn't by yourself please contact the admin."
                        send_mail(message, email)
                except Exception as e:
                    errors.append(str(e))
                    user_obj = user.objects.create(email=email, phone_model=phone)

                refresh = RefreshToken.for_user(user_obj)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user_obj, many=False).data
                }
                #delete OTP
            else:
                #login failed
                data = {
                    'msg': 'Wrong OTP'
                }

        except Exception as e:
            errors.append(str(e))
            data = {
                'msg': 'Try Sending OTP First',
                'errors': errors
            }

        return Response(data, status=status.HTTP_200_OK)

class AccountDeleteAPI():

    authentication_classes = [JWTAuthentication]

    def delete(self, request):
        user_id = request.user.id

        try:
            user_obj = user.objects.get(id=user_id)
            user_obj.delete()
            msg = 'User Deleted'
        except Exception as e:
            msg = str(e)

        return Response(data={'msg':msg}, status=status.HTTP_200_OK)
