from django.contrib import admin
from .models import User, Tenant
# Register your models here.
admin.site.register(User)
admin.site.register(Tenant)