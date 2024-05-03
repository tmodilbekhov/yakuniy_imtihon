from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import CreatePostSerializer, UpdatePostSerializer, AllPostSerializer, AddLikeSerializer, \
    UserSerializer, CommentSerializer, GetAllCommentSerializer
from rest_framework.response import Response
from .models import Post, Like, Comment
from rest_framework import status
from django.contrib.auth.models import User

class PostApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        user = request.user

        request.data['user'] = user.id

        serializer = CreatePostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class PostUpdateView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, id):
        post = get_object_or_404(Post, id=id)
        data = request.data
        serializer = UpdatePostSerializer(instance=post, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class PostDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()

        return Response({'message': 'Post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class AllPostsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        posts = Post.objects.all()
        serializer = AllPostSerializer(posts, many=True)
        return Response(serializer.data)



class AddLikeView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        user = request.user
        if Like.objects.filter(post=post, user=user).exists():
            return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

        like = Like(post=post, user=user)
        like.save()
        serializer = AddLikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Get_users_who_liked(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        liked_users = User.objects.filter(likelar__post=post)
        serializer = UserSerializer(liked_users, many=True)

        return Response(serializer.data)


class AddCommentView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        user = request.user
        comment_content = request.data.get('comment', '')
        comment = Comment(post=post, user=user, comment=comment_content)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class GetAllPostCommentaryView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        post_comments = Comment.object.filter(post=post)
        serializer = GetAllCommentSerializer(post_comments, many=True)
        return Response(serializer.data)
