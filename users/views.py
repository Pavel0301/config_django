from django.shortcuts import get_object_or_404

from django.views.generic import DetailView, ListView

from users.users import User, Profile



class UserProfileDetailView(DetailView):
    model = User
    template_name = 'users/user_profile.html'
    context_object_name = 'user'


user_profile_detail_view = UserProfileDetailView.as_view()


class UserFriendsListView(ListView):
    model = Profile
    template_name = 'users/user_friends_list_view.html'
    context_object_name = 'friends'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_object_or_404(Profile, )


user_friends_list_view = UserFriendsListView.as_view()
