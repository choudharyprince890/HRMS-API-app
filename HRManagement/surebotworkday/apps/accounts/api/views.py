from cgitb import reset
import email
import requests
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_400_BAD_REQUEST 
from rest_framework.permissions import IsAuthenticated, AllowAny
# for class 
from rest_framework.views import APIView
from rest_framework import status   
from rest_framework import generics,status

from surebotworkday.apps.accounts.models import Tenant

from .serializer import UserRegisterSerializer,TenantSerializer,UserLoginSerializers, UserListSerializer, ResetPasswordOtpSerializer,UserRegisterSerializerOTP
from surebotworkday.apps.accounts.models import User

# from surebotworkday.apps.accounts.api import serializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.db import transaction

# from HRManagement.surebotworkday.apps.accounts.api import serial izer

# register API 
class userRegister(generics.GenericAPIView):
    serializer_class = TenantSerializer
    permission_classes = (AllowAny, )
    @swagger_auto_schema(operation_description="Register API")

    def post(self, request):
        with transaction.atomic():
            user_serializer = UserRegisterSerializer(data=request.data)
            print("ok",user_serializer)
            # print("ok 222",user_serializer.data)
            if user_serializer.is_valid():
                user_serializer.save()
                print("only data",user_serializer.data)
                user = user_serializer.data['id']
                print("user_serializer id",user)
                request.data._mutable = True
                request.data['user'] = user
                serializer = self.serializer_class(data=request.data)
                valid = serializer.is_valid(raise_exception=True)
                if valid:
                    serializer.save()
                    status_code = status.HTTP_201_CREATED
                    response = {
                        'success': True,
                        'statusCode': status_code,
                        'message': 'User successfully registered!',
                    }
                    return Response(response, status=status_code)
            else:
                return Response(user_serializer.errors)  


# class userRegister(generics.GenericAPIView): 
#     quesryset = User.objects.all()
#     serializer_class = UserRegisterSerializer

# class TenantRegister(generics.GenericAPIView):
#     quesryset = Tenant.objects.all()
#     serializer_class = TenantSerializer




# login API 
class userLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializers
    permission_classes = (AllowAny, )
    @swagger_auto_schema(operation_description="Login API")
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            status_code = status.HTTP_200_OK
            response = {
                'success': True,
                'statusCode': status_code,
                'message': 'User logged in successfully',
                'access': serializer.data['access'],
                'refresh': serializer.data['refresh'],
                'authenticatedUser': {
                    'email': serializer.data['email'],
                    'role': serializer.data['role']
                }
            }
            return Response(response, status=status_code)
            # return render Response(response, status=status_code)
        else:
            return Response(serializer.errors) 


  

# user list API 
class userList(APIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)
    access_token = openapi.Parameter('access token', in_=openapi.IN_QUERY, description='Access Token',type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[access_token])
    def get(self, request):
        user = request.user
        print(request.user.role != 1,request.user.role)
        if int(request.user.role) != 1:
            response = {
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = User.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                'success': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Successfully fetched users',
                'data': serializer.data
                }
            return Response(response, status=status.HTTP_200_OK)




#  change password

# class ChangePasswordView(UpdateAPIView):
#         serializer_class = ChangePasswordSerializer
#         model = User
#         permission_classes = (IsAuthenticated,)

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj

#         def update(self, request):
#             self.object = self.get_object()
#             serializer = self.get_serializer(data=request.data)

#             if serializer.is_valid():
#                 if not self.object.check_password(serializer.data.get("old_password")):
#                     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                 self.object.set_password(serializer.data.get("new_password"))
#                 self.object.save()
#                 response = {
#                     'status': 'success',
#                     'code': status.HTTP_200_OK,
#                     'message': 'Password updated successfully',
#                     'data': []
#                 }
#                 return Response(response)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# from .serializer import UserPasswordChangeSerializer
# from rest_framework.generics import UpdateAPIView

# class APIChangePasswordView(APIView):
#     # def post(self,request,*args,**kwargs):
#     #     data = request.data
#     serializer_class = UserPasswordChangeSerializer
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         print('data.. ',serializer.data)
#         user = User.objects.all()
#         if serializer.is_valid():
#             serializer.save()
#             pas = serializer.data['new_password']
#             # if not self.object.check_password(serializer.data.get("password")):
#             #     return Response({"password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # self.object.set_password(pas)    

#             status_code = status.HTTP_200_OK
#             response = {
#                 'success': True,
#                 'statusCode': status_code,
#                 'message': 'Password changed successfully',
#             }
#             return Response(response, status=status_code)
#         else:
#             return Response(serializer.errors) 



from django.contrib.auth import authenticate

class ChangePasswordAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,*args,**kwargs):
        data = request.data
        print ("dataaaa",data)  
        d_user = request.user
        password = data['current_password']
        new_password = data['new_password']
        # user = User.objects.get(email=d_user.email)
        user = authenticate(email=d_user.email, password=password)
        print ("dataaaa",user)
        if user is not None:
            if user.is_active:
                # self.auth_login(request,user)
                user.set_password(new_password) 
                user.save()
                return Response({'response':'Password Changed'},status=HTTP_200_OK)
            else:
                print("The username and password were incorrect.")
                return Response({'error':'User not active'},status=HTTP_400_BAD_REQUEST)
        else:
            print("The password were incorrect.")
            return Response({'login_response':'password is incorrect'},status=HTTP_400_BAD_REQUEST)



# send email otp
# from .email import *

# class SendOtp(APIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = ResetPasswordOtpSerializer
#     def post(self, request):
#         query_set = User.objects.get(email=request.user.email)
#         # id_set = User.objects.get(user=request.user.pk)
#         # print('this is the id_set ',id_set.pk)
#         print('this is query_set...',query_set)
#         user_detail = UserRegisterSerializerOTP(query_set, many=True)
#         print('this is the user_email...', user_detail)
#         # serializer = self.serializer_class(data=request.data)
#         serializer = self.serializer_class(user_detail, many=True)
#         print('this is serializer...', serializer)
#         if serializer.is_valid():
#             serializer.save()
#             send_otp(query_set)
#             status_code = status.HTTP_200_OK
#             response = {
#                     'success': True,
#                     'statusCode': status_code,
#                     'message': 'Email sent successfully',
#                 }
#             return Response(response, status=status_code)
#         else:
#             status_code = status.HTTP_403_FORBIDDEN
#             response = {
#                 'success': False,
#                 'statusCode': status_code,
#                 'message': 'something went wrong'
#             } 
#             return Response(serializer.errors, status=status_code)





from .email import *

class SendOtp(APIView):
# class SendOtp(generics.GenericAPIView):
    # rest_serializer = ResetPasswordOtpSerializer
    permission_classes = (IsAuthenticated,) 
    def post(self, request):
        query_set = User.objects.get(email=request.user.email)
        print('this is the queryset ',query_set)
        id_no = request.user.pk
        print('id no is ...', id_no)
        send_otp(query_set)
        # send_otp()
        status_code = status.HTTP_200_OK
        response = {
                    'success': True,
                    'statusCode': status_code,
                    'message': 'Email sent successfully',
                }
        return Response(response, status=status_code)
 
  


class verifyOTPView(APIView):
    def post(self, request):
        # username = request.data["username"]
        otp = int(request.data["otp"])
        user = User.objects.get(email=request.user.email)
        print('this is user..' ,user)
        print('this is user pk' ,user.pk)
        pkexist = ResetPasswordOtp.objects.filter(user_id = user.pk)
        print('this is pk in pass table..', pkexist[0].otp)
        tableotp = (pkexist[0].otp)
        if tableotp==otp:
            print('done here')
            # user.verified = True
            #user.otp.delete()
            # user.save()
            return Response("Verification Successful", status=HTTP_200_OK)
        else:
            print('done else')
            raise Response('OTP Varification Failed', status=HTTP_400_BAD_REQUEST)