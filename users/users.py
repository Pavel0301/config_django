from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from phonenumber_field.modelfields import PhoneNumberField

from users.managers import CustomUserManager



class User(AbstractUser):
    """ Модель пользователя """
    username = models.CharField(
        verbose_name='Никнейм', max_length=64, unique=True, null=True, blank=True
    )
    email = models.EmailField(verbose_name='Почта', unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(verbose_name='Телефон', unique=True, null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        """ Мета-класс Пользователя """
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        new_user = self.pk is None
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(self.username)
            super().save(*args, **kwargs)
        if new_user:
            Profile.objects.create(user=self)


class Profile(models.Model):
    """ Модель профиля пользователя """
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, verbose_name='Профиль', related_name='profile'
    )

    bio = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telegram ID')
    instagram_link = models.URLField(blank=True, null=True)

    class Meta:
        """ Мета-класс модели профиля """
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f'{self.user} ({self.pk})'



