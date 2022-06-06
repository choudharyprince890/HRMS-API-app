from dataclasses import field
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from surebotworkday.apps.accounts.models import Tenant, ResetPasswordOtp
# from accounts.models import ResetPasswordOtp
from surebotworkday.apps.accounts.models import User
from django.contrib.auth.hashers import make_password


#  creating serializers 
#  register serializers
'''class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
    
    def create(self, validated_data):
        auth_user = User.objects.create_user(**validated_data)
        return auth_user'''


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','password','role')

        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data): 
        user = User.objects.create(
            email=validated_data['email'],
            password = make_password(validated_data['password']),
            role=validated_data['role'],
        )
        return user

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = ('name','email', 'status', 'domain', 'valid_upto', 'created_on', 'user') 


# login serializer
class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True) 
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass
    def validate(self, data):
        email = data['email']
        password = data['password']
        user = authenticate(email=email, password=password)
        print(user,"user")
        if user is None:
            print('uphere')
            raise serializers.ValidationError("Invalid Login Credentials...")     
        try:
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)
            
            validation = {
                'access': access_token, 
                'refresh': refresh_token,
                'email': user.email,
                'role': user.role,
                }
            return validation
        except User.DoesNotExist:
            print('downhere')
            raise serializers.ValidationError("Invalid Login Credentials")

# users list serializers 
class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','role']


# send otp email
class UserRegisterSerializerOTP(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email')

class ResetPasswordOtpSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResetPasswordOtp
        fields = ('otp', 'user', 'time')



# change password
# '''class ChangePasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(write_only=True, required=True)
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = User
#         fields = ('old_password', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})
#         return attrs

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value

#     def update(self, instance, validated_data):
#         instance.set_password(validated_data['password'])
#         instance.save()
#         return instance'''




# class UserPasswordChangeSerializer(serializers.Serializer):
#     # password = serializers.CharField(max_length=150, write_only=True)
#     new_password = serializers.CharField(required=True, max_length=30)
#     confirmed_password = serializers.CharField(required=True, max_length=30)
#     class Meta:
#         model = User
#         fields = ('new_password', 'confirmed_password', 'password')
#         print('ok')

#     def create(self, validated_data):
#         pass
#     def validate(self, data):
#         print('here...')
#         if data['new_password'] != data['confirmed_password']:
#             raise serializers.ValidationError("passwords didn't match")
#         return data

#     def validate_password(self, data):
#         print("comes here...")
#         if not self.context['request'].user.check_password(data.get('password')):
#             raise serializers.ValidationError("old password os wrong")

#     def update(self, instance, validated_data):
#         instance.set_password(validated_data['new_password'])
#         instance.save()
#         return instance
#     @property
#     def data(self):
#         return {'Success': True}





# class resetpasswordSerializer(serializers.ModelSerializer):
#     username=serializers.CharField(max_length=100)
#     changepassword=serializers.CharField(max_length=100)
#     changepassword=serializers.CharField(max_length=100)
#     class Meta:
#         model=User
#         fields=('username', 'password', 'changepassword')
#         def save(self):
#             username=self.validated_data['username']
#             password=self.validated_data['password']
#             if User.objects.filter(username=username).exists():
#                 user=User.objects.get(username=username)
#                 user.set_password(password)
#                 user.save()
#                 return user
#             else:
#                 raise serializers.ValidationError({'error':'please enter valid crendentials'})

# class resetpasswordSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=User
#         fields=('username', 'password', 'changepassword')