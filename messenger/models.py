from django.db import models
from django.utils.text import slugify

from services.common.dicts import CHAT_ROOM_MAX_NAME
from messenger.managers import MessageManager
from users.models import User


class MessengerRoom(models.Model):
    """  Модель чат-комнаты """

    class MessengerRoomType(models.TextChoices):
        DIRECT_ROOM = 'dr', 'direct_room'
        COMMON_ROOM = 'cr', 'common_room'

    admin_room = models.ForeignKey(
        to=User, on_delete=models.RESTRICT, verbose_name='Админ чата', related_name='admin_room'
    )
    name = models.CharField(max_length=CHAT_ROOM_MAX_NAME, unique=True, blank=True, null=True)
    participants = models.ManyToManyField(to=User, blank=False)
    room_type = models.CharField(max_length=2, choices=MessengerRoomType.choices, default=MessengerRoomType.DIRECT_ROOM)

    slug = models.SlugField(max_length=40, unique=True)

    class Meta:
        verbose_name = 'Чат-комната'
        verbose_name_plural = 'Чат-комнаты'

    @property
    def participants_count(self):
        """ подсчет участников комнаты """
        return self.participants.count()

    def __str__(self):
        return f'{self.name} ({self.room_type}'

    def save(self, *args, **kwargs):
        #new_room = self.pk is None
        #super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.name)
            super().save(*args, **kwargs)




class Message(models.Model):
    """ Модель собщений """

    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE, verbose_name='Автор сообщения', related_name='message_author'
    )
    room = models.ForeignKey(
        to=MessengerRoom, on_delete=models.CASCADE, verbose_name='Комната чата', related_name='room_m'
    )
    content = models.TextField()
    #read_users = models.ManyToManyField(
    #    User, related_name='messages_read_users'
    #)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

    class Meta:
        verbose_name ='Сообщение'
        verbose_name_plural = 'Сообщения'

        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.text} [{self.timestamp}]'



