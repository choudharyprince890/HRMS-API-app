from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from datetime import date, datetime

from django.forms import CharField
from.manager import AccountManager
from django.utils import timezone
import uuid

class User(AbstractBaseUser, PermissionsMixin):
    ADMIN = 1
    EMPLOYEE = 2

    ROLE = (
        (ADMIN, 'admin'),
        (EMPLOYEE, 'employee')
    )
    uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public Id')
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, default='2', choices=ROLE)
    designatin = models.CharField(blank = True, max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    @property
    def is_staff(self):
        return self.is_active

    objects = AccountManager()

class Tenant(models.Model):
    Delete_STATUS = (
    ('Active', 'Active'),
    ('InActive', 'InActive')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    status  = models.CharField(max_length=100, default='Active', choices=Delete_STATUS)
    domain = models.CharField(max_length=100, unique=True)
    valid_upto = models.DateField()
    created_on = models.DateTimeField(default=datetime.now)



class ResetPasswordOtp(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, blank=True, null=True)
    time = models.DateTimeField(default=timezone.now)