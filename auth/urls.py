from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.user_login, name='auth_login'),
    path('signup/', views.user_signup, name='auth_signup'),
    path('logout/', views.user_logout, name='auth_logout'),
    path('', include('allauth.urls'), name='auth_account'),
]