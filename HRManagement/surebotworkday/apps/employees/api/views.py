from rest_framework.response import Response
from rest_framework import generics,status
from surebotworkday.apps.accounts.api.serializer import UserListSerializer

from surebotworkday.apps.accounts.models import Tenant
from .serializer import employeeDetailSerializer, employeeListSerializer, TenantSerializer, UserRegisterSerializer
from surebotworkday.apps.employees.models import Employee_detail
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from surebotworkday.apps.accounts.models import User

# from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# #    User detail API 
# class employeeDetails(generics.GenericAPIView):
#     employee_detail_serializer = employeeDetailSerializer
#     tenent_register_serializer = TenantSerializer
#     # permission_classes = (IsAuthenticated, )
#     permission_classes = (AllowAny, )
#     @swagger_auto_schema(operation_description="Employee details API")
#     def post(self,request):
#         user_register = UserRegisterSerializer(data=request.data)
#         print('ok1',user_register)
#         if user_register.is_valid():
#             print('ok2')
#             user_register.save()
#             print("user register id", user_register.data)
#             user_register_id = user_register.data['id']
#             print("user register id", user_register_id)
#             request.data._mutable = True
#             request.data['user'] = user_register_id
#             tenent_data = self.tenent_register_serializer(data=request.data)
#             if tenent_data.is_valid():
#                 tenent_data.save()
#                 tenent_data_id = tenent_data.data['id']
#                 print('tenant id', tenent_data_id)
#                 request.data._mutable = True
#                 request.data['tenant'] = tenent_data_id
#                 employee_detail = self.employee_detail_serializer(data=request.data)
#                 if employee_detail.is_valid():
#                     employee_detail.save()
#                     status_code = status.HTTP_201_CREATED
#                     response = {
#                         'success': True,
#                         'statusCode': status_code, 
#                         'message': 'Detailes are filled!',
#                     }
#                     return Response(response, status=status_code)
#             else:
#                 return Response(tenent_data.errors, status=status.HTTP_403_FORBIDDEN)
#         else:
#             return Response(user_register.errors, status=status.HTTP_403_FORBIDDEN)        


#  Employee Details API 
class employeeDetails(generics.GenericAPIView):
    employee_detail_serializer = employeeDetailSerializer
    tenent_register_serializer = TenantSerializer
    permission_classes = (IsAuthenticated, )
    access_token = openapi.Parameter('access token', in_=openapi.IN_QUERY, description='Access Token',type=openapi.TYPE_STRING)
    @swagger_auto_schema(operation_description="Employee details API")
    def post(self,request):
        print("user pk",request.user.pk) 
        tenant = Tenant.objects.get(user=request.user.pk)
        print("Tenent pk",tenant.pk)
        user_register = UserRegisterSerializer(data=request.data)
        print('ok1',user_register)
        if user_register.is_valid():
            print('ok2') 
            user_register.save()
            print("user register id", user_register.data)
            user_register_id = user_register.data['id']
            print("user register id", user_register_id)
            request.data._mutable = True
            request.data['user'] = user_register_id
            request.data['tenant'] =tenant.pk
            employee_detail = self.employee_detail_serializer(data=request.data)
            if employee_detail.is_valid():
                employee_detail.save()
                status_code = status.HTTP_201_CREATED
                response = {
                    'success': True,
                    'statusCode': status_code, 
                    'message': 'Detailes are filled!',
                }
                return Response(response, status=status_code)
            else:
                return Response(employee_detail.errors, status=status.HTTP_403_FORBIDDEN)        

        else:
            return Response(user_register.errors, status=status.HTTP_403_FORBIDDEN)        





# class SnippetFilters(filters.FilterSet):
#     title = filters.CharFilter(lookup_exp='icontains')
#     class Meta:
#         model = Employee_detail
#         fileds = ('designation',)





# #  Employee Details list API 
# class employeeList(generics.ListAPIView): 
#     serializer_emp = employeeListSerializer
#     filter_backends = [DjangoFilterBackend]
#     # filterset_class = SnippetFilters
#     filterset_fields = ['designation']
#     # permission_classes = (AllowAny,)
#     def get(self,request):
#         employee = Employee_detail.objects.all()
#         serializer = self.serializer_emp(employee, many=True)
#         response = {
#             'success': True,
#             'status_code': status.HTTP_200_OK,
#             'message': 'Successfully fetched users',
#             'data': serializer.data
#             }
#         return Response(response, status=status.HTTP_200_OK)




class employeeList(generics.ListAPIView):
    serializer_class = employeeListSerializer
    serializer_userlist = UserListSerializer
    queryset = Employee_detail.objects.all()
    permission_classes = (IsAuthenticated, )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['designation', ]

    def get_queryset(self):
        print('ok')
        users = User.objects.all()
        print('this are users ',users)
        # serializer = self.serializer_userlist(users, many=True)
        print("data of user objct....", users)
        # print('serializer data....', serializer)
        if int(self.request.user.role) == 1:
            # print(self.request.user.role)
            return self.queryset


# class employeeDetails(generics.GenericAPIView):
#     employee_detail_serializer = employeeDetailSerializer
#     tenent_register_serializer = TenantSerializer
#     permission_classes = (IsAuthenticated, )
#     access_token = openapi.Parameter('access token', in_=openapi.IN_QUERY, description='Access Token',type=openapi.TYPE_STRING)
#     @swagger_auto_schema(operation_description="Employee details API")
#     def post(self,request):
#         print("user pk",request.user.pk)
#         tenant = Tenant.objects.get(user=request.user.pk)
#         print("Tenent pk",tenant.pk)
#         user_register = UserRegisterSerializer(data=request.data)
#         print('ok1',user_register)
#         if user_register.is_valid():
#             print('ok2')
#             user_register.save()
#             print("user register id", user_register.data)
#             user_register_id = user_register.data['id']
#             print("user register id", user_register_id)
#             request.data._mutable = True
#             request.data['user'] = user_register_id
#             request.data['tenant'] =tenant.pk
#             employee_detail = self.employee_detail_serializer(data=request.data)
#             if employee_detail.is_valid():
#                 employee_detail.save()
#                 status_code = status.HTTP_201_CREATED
#                 response = {
#                     'success': True,
#                     'statusCode': status_code, 
#                     'message': 'Detailes are filled!',
#                 }
#                 return Response(response, status=status_code)
#             else:
#                 return Response(employee_detail.errors, status=status.HTTP_403_FORBIDDEN)        

#         else:
#             return Response(user_register.errors, status=status.HTTP_403_FORBIDDEN)      
# 