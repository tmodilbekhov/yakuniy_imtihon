from django.urls import path
from .views import PostApiView, PostUpdateView, PostDeleteView, AllPostsView, AddLikeView, Get_users_who_liked, AddCommentView, GetAllPostCommentaryView

app_name = 'posts'

urlpatterns = [
    path('create-post/', PostApiView.as_view(), name='create'),
    path('update-post/<int:id>/', PostUpdateView.as_view(), name='update'),
    path('delete-post/<int:id>/', PostDeleteView.as_view(), name='delete'),
    path('all-view/', AllPostsView.as_view(), name='allgetsposts'),
    path('like/<int:id>/', AddLikeView.as_view(), name='addlike'),
    path('liked-users/<int:id>/', Get_users_who_liked.as_view(), name='likedusers'),
    path('comments/<int:id>/', AddCommentView.as_view(), name='addcomments'),
    path('comments/<int:id>/', GetAllPostCommentaryView.as_view(), name='post-comments'),
]
