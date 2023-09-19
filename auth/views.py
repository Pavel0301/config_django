from allauth.account.views import SignupView, LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy


class UserLoginView(LoginView):
    template_name = 'auth/login.html'


user_login = UserLoginView.as_view()


class UserSignupView(SignupView):
    template_name = 'auth/signup.html'


user_signup = UserSignupView.as_view()


class UserLogoutView(LogoutView):
    next_page = ('auth_login')


user_logout = UserLogoutView.as_view()
