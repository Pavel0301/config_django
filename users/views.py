import pdb

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.views.generic import DetailView

from users.models import User, Profile



class UserProfileDetailView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'


user_profile_detail_view = UserProfileDetailView.as_view()


