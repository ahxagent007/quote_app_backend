import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .email import send_mail


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
            'email': 'ahx.agent007@gmail.com'
        }
        '''

        email = request.data['email']

        message = 'Your Quote App OTP is {0}'.format(123456)
        send_mail(message, email)

        data = {}
        return Response(data, status=status.HTTP_200_OK)