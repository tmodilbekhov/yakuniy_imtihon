from django.urls import path
from .views import LoginApiView, RegisterApiView, GetAllUsersView, SendFriendRequest

app_name = 'users'

urlpatterns = [
    path('login/', LoginApiView.as_view(), name='login'),
    path('register/', RegisterApiView.as_view(), name='register'),
    path('get-users/', GetAllUsersView.as_view(), name='get_all_users'),
    path('send-friend-request/<int:id>/', SendFriendRequest.as_view(), name='send-friend-request'),
]
