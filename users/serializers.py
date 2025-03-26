from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime, timedelta

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token = self.get_token(self.user)
        refresh_token = self.get_token(self.user)
        
        access_token.set_exp(lifetime=timedelta(seconds=20))
        refresh_token.set_exp(lifetime=timedelta(minutes=1))
        
        data['access_expires'] = (datetime.now() + timedelta(seconds=20)).isoformat()
        data['refresh_expires'] = (datetime.now() + timedelta(minutes=1)).isoformat()
        
        return data