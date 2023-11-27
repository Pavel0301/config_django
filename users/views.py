from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from config import settings
from users.forms import EditUserInfoForm, EditProfileInfoForm
from users.models import User, Profile
from django.contrib import messages

def get_user_context_object_name():
    return getattr(settings, 'USER_CONTEXT_OBJECT_NAME', 'user')

@login_required(login_url='auth_login')
def view_user_profile(request, username, template_name='users/user_profile.html'):
    user = get_object_or_404(User, username=username)
    profile_context = User.objects.profile(user)

    return render(
        request,
        template_name,
        {
            get_user_context_object_name(): user,
            'user_context_object_name': get_user_context_object_name(),
            'profile': profile_context,
            'username': username

        }
    )

@login_required(login_url='auth_login')
def edit_user_profile(request, username, template_name='users/user_profile_edit.html'):
    us_form = EditUserInfoForm(request.POST, instance=request.user)
    pr_form = EditProfileInfoForm(request.POST, request.FILES, instance=request.user.profile)

    if request.method == 'POST':

        if us_form.is_valid() and pr_form.is_valid():
            us_form.save()
            pr_form.save()
            messages.success('Вы успешно изменили данные пользователя')
            return redirect(to='view_user_profile')

    else:
        return render(request, template_name, context={'us_form': us_form,
                                                       'pr_form': pr_form,
                                                       'username': username})



