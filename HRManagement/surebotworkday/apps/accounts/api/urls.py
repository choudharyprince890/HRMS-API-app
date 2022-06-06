from unicodedata import name
from django import views
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

from surebotworkday.apps.accounts.api.views import *

# from rest_framework.routers import DefaultRouter
# router = DefaultRouter()    
# router.register('user', userRegister.as_view(), basename='user')
# router.register('tenant', TenantRegister.as_view(), basename='tenant')






urlpatterns = [
    path('token/obtain', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('register', userRegister.as_view()),
    # path('changepass', changePassword.as_view()),
    path('changepass', ChangePasswordAPIView.as_view()),
    path('sendmail', SendOtp.as_view()),
    path('verifyotp', verifyOTPView.as_view()),
    # path('register',include(router.urls)),
    path('login', userLogin.as_view()),
    path('users', userList.as_view()),
]

