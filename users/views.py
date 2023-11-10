from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from django.views.generic import DetailView, ListView

from config import settings
from users.models import User, Profile

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
        }
    )
