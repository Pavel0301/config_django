from django.urls import path
from friendship.views import (
    all_users,
    view_friends,
    friendship_add_friend,
    friendship_request_list,
    friendship_request_detail,

)

urlpatterns = [
    path('users/', all_users, name='friendship_view_users'),
    path('friends/<slug:username>/', view_friends, name='friendship_view_friends'),
    path('friend/add/<slug:to_username>/', friendship_add_friend, name='friendship_add_friend'),
    path("friend/requests/", friendship_request_list, name="friendship_request_list"),
    path('friend/request/<int:friendship_request_id>', friendship_request_detail, name="friendship_request_detail"),

]
