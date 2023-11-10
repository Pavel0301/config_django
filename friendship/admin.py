from django.contrib import admin

from friendship.models import Friend, Follow, FriendshipRequest


# Register your models here.

class FriendAdmin(admin.ModelAdmin):
    model = Friend
    raw_id_fields = ('to_user', 'from_user')



class FollowAdmin(admin.ModelAdmin):
    model = Follow
    raw_id_fields = ('follower', 'followee')


class FriendRequestAdmin(admin.ModelAdmin):
    model = FriendshipRequest
    raw_id_fields = ('from_user', 'to_user')

admin.site.register(Follow, FollowAdmin)
admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendshipRequest, FriendRequestAdmin)
