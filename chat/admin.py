from django.contrib import admin
"""
from chat.models import Room, Message


#from chat.models import Room, Message


# Register your models here.

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'room']
"""