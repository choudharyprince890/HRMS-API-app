from datetime import datetime
from enum import unique
from django.db import models

from surebotworkday.apps.accounts.models import Tenant, User
# from accounts.models import User, Tenant
# from apps import accounts

# Create your models here.
Delete_STATUS = (
    ('Active', 'Active'),
    ('Away', 'Away')
)
ROLES = (
    ('Manager', 'Manager'),
    ('HR', 'HR'),
    ('Web Developer', 'Web Developer'),
    ('Android Developer', 'Android Developer'),
    ('Tester', 'Tester')
)


class Employee_detail(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField(max_length=200)
    joining_date = models.DateField(default=datetime.now)
    designation = models.CharField(max_length=30)
    status  = models.CharField(max_length=50, default='Active', choices=Delete_STATUS)
    role = models.CharField(max_length=50, choices=ROLES, default='Web Developer')
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table='Employee Details'



