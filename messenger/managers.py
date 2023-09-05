from django.db import models


class MessageManager(models.Manager):
    """ Менеджер для модели Message """

    def create(self, **kwargs):
        message = super().create(**kwargs)
        message.read_users.set([message.user])
        return message

    def validate_messanger_room_name(self):
        pass
