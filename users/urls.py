from django.urls import path
from .views import (
    view_user_profile,
    edit_user_profile
)


urlpatterns = [
    path('<slug:username>/', view_user_profile, name='view_user_profile'),
    path('<slug:username>/edit/', edit_user_profile, name='edit_user_profile')
]
