from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.validators import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import FriendRequest

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, min_length=4)
    password = serializers.CharField(min_length=4)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            data = {
                "status":False,
                "message":"User not found"
            }

            raise ValidationError(data)
        attrs['user'] = user

        return attrs

    def to_representation(self, instance):

        user = instance['user']
        refresh = RefreshToken.for_user(user)

        data = {
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

        return data

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, min_length=4, required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(max_length=20, required=True)
    confirm_password = serializers.CharField(max_length=20, required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if confirm_password != password:
            data = {
                "status":False,
                "message":"Passwords don't match"
            }

            raise ValidationError(data)

        return attrs

    def validate_username(self, username):

        if username.startswith('@') or username.startswith('!'):
            data = {
                "status":False,
                "message":"Username is not valid"
            }

            raise ValidationError(data)

        return username

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']

        user = User()
        user.username = username
        user.email = email
        user.set_password(password)
        user.save()

        return user

    def to_representation(self, instance):

        refresh = RefreshToken.for_user(instance)

        data = {
                "status":True,
                "message":"User registered successfully",

                "tokens":{
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['sender', 'receiver', 'created_at']