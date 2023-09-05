from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from auth.forms import UserRegForm, UserLoginForm


# Create your views here.


def user_reg(request):
    """ регистрация пользователя """

    """if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_profie'))"""
    reg_form = UserRegForm(request.POST)
    if not request.method == 'POST':
        context = {
            'reg_form': reg_form,
        }
        return render(request, 'frontend/templates/auth/user_reg.html', context)
    else:
        if reg_form.is_valid():
            user = reg_form.save(commit=False)
            user.set_password(user.password)
            user.save()
            message = 'Please check your profile information'

            context = {
                'message': message,
            }
            return render(request, 'frontend/templates/users/user_profile.html', context)


def user_login(request):
    """if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user_profile'))"""
    log_form = UserLoginForm(request.POST)
    if not request.method == 'POST':
        context = {
            'log_form': log_form,
        }
        return render(request, 'frontend/templates/auth/user_login.html', context)
    else:
        if log_form.is_valid():
            pass

