from rest_framework import serializers
from .models import Post, Like, Comment
from django.contrib.auth.models import User
class CreatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['user', 'content']

class UpdatePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']


class DeletePostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['content']


class AllPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['user', 'content', 'created_at']


class AddLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'comment']


class GetAllCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['user', 'comment']
