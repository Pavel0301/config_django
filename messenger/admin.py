from django.contrib import admin
from messenger.models import MessengerRoom, Message


@admin.register(MessengerRoom)
class MessengerRoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']


