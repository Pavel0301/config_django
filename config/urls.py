from django.contrib import admin
from django.urls import path, include
from auth.urls import urlpatterns as auth_urls
from users.urls import urlpatterns as users_urls
from blog.urls import urlpatterns as blog_urls
from friendship.urls import urlpatterns as friendship_urls
#from messenger.urls import urlpatterns as messenger_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    #path('', include('chat.urls')),
    #path('', include('users.urls')),

]
urlpatterns += friendship_urls
urlpatterns += blog_urls
urlpatterns += auth_urls
urlpatterns += users_urls
#urlpatterns += messenger_urls


