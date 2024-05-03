from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, FriendRequestSerializer
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import FriendRequest


class LoginApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class RegisterApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetAllUsersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class SendFriendRequest(APIView):
    def post(self, request, id):
        user_id = request.data.get('user_id')
        follow_user_id = request.data.get('follow_user_id')
        from django.shortcuts import get_object_or_404
        user = get_object_or_404(User, id=user_id)
        follow_user = get_object_or_404(User, id=follow_user_id)
        if FriendRequest.objects.filter(sender=user, receiver=follow_user).exists():
            return Response({'message': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
        friend_request = FriendRequest(sender=user, receiver=follow_user)
        friend_request.save()
        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
