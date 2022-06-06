from dataclasses import field
from xml.parsers.expat import model
from django.forms import modelformset_factory
from rest_framework import serializers
from surebotworkday.apps.employees.models import Employee_detail

from surebotworkday.apps.accounts.models import Tenant, User


# from django_filters import rest_framework as filters



class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        # fields = ('id', 'name', 'email', 'status', 'domain', 'valid_upto', 'created_on', 'user')
        fields = ('id', 'user')
class employeeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_detail
        fields = ('first_name', 'last_name', 'dob', 'email', 'phone', 'address', 'joining_date', 'designation', 'status', 'role', 'is_delete', 'user', 'tenant')
        


class employeeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_detail
        # fields = ('first_name','last_name')
        fields = '__all__'



