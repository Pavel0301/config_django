from django.urls import path
from .views import (
    view_user_profile
)


urlpatterns = [
    path('<slug:username>/', view_user_profile, name='view_user_profile'),
]
