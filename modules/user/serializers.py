from rest_framework import serializers
from core.utils.exception_utils import AppExceptionHelper, AppValidateException
from modules.user.models import CustomUserModel as User

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
           'id', 
           'username', 
           'email',
           'password', 
           'first_name', 
           'last_name', 
           'last_login',
           'is_active', 
           'role', 
           'created_at', 
           'updated_at'
        ]
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
    def validate(self, attrs):
        return super().validate(attrs)