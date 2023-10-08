from django.urls import path
from . import views


urlpatterns = [
    path('<slug:slug>/', views.user_profile_detail_view, name='user_profile'),
    path('friends/', views.user_friends_list_view, name='user_friends_list_view'),
]
