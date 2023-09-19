from django.urls import path
from . import views


urlpatterns = [
    path('feed/', views.feed_list_view, name='feed_list_view'),
    path('feed/<slug:slug>/', views.feed_detail_view, name='feed_detail_view'),
]
