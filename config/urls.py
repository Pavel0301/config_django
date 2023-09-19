from django.contrib import admin
from django.urls import path
from auth.urls import urlpatterns as auth_urls
from users.urls import urlpatterns as users_urls
from blog.urls import urlpatterns as blog_urls

urlpatterns = [
    path("admin/", admin.site.urls),

]

urlpatterns += blog_urls
urlpatterns += auth_urls
urlpatterns += users_urls


