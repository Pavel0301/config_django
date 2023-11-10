import pdb

from django.core.exceptions import ValidationError
from django.db import models
from users.models import User
from config import settings
from django.core.cache import cache
from django.db.models import Q
from django.utils import timezone
from friendship.exceptions import AlreadyExistsError, AlreadyFriendsError

from friendship.signals import (
    friendship_request_created,
    friendship_removed,
    follower_created,
    followee_created,
    following_created,
    follower_removed,
    followee_removed,
    following_removed,
    friendship_request_viewed,
    friendship_request_canceled,
    friendship_request_rejected,
    friendship_request_accepted
)

CACHE_TYPES = {
    "friends": "f-%s",
    "followers": "fo-%s",
    "following": "fl-%s",
    "blocks": "b-%s",
    "blocked": "bo-%s",
    "blocking": "bd-%s",
    "requests": "fr-%s",
    "sent_requests": "sfr-%s",
    "unread_requests": "fru-%s",
    "unread_request_count": "fruc-%s",
    "read_requests": "frr-%s",
    "rejected_requests": "frj-%s",
    "unrejected_requests": "frur-%s",
    "unrejected_request_count": "frurc-%s",
}

BUST_CACHES = {
    "friends": ["friends"],
    "followers": ["followers"],
    "blocks": ["blocks"],
    "blocked": ["blocked"],
    "following": ["following"],
    "blocking": ["blocking"],
    "requests": [
        "requests",
        "unread_requests",
        "unread_request_count",
        "read_requests",
        "rejected_requests",
        "unrejected_requests",
        "unrejected_request_count",
    ],
    "sent_requests": ["sent_requests"],
}


def cache_key(type, user_pk):
    """
    Создаёт ключ кэша для определенного типа кэшированного значения
    """
    return CACHE_TYPES[type] % user_pk


def bust_cache(type, user_pk):
    """
     Перебор нашего кэша для заданного типа, может перебрать несколько кэшей
    """
    bust_keys = BUST_CACHES[type]
    keys = [CACHE_TYPES[k] % user_pk for k in bust_keys]
    cache.delete_many(keys)


class FriendshipRequest(models.Model):
    """Модель для предоставления запросов дружбы"""
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='friendship_request_sent')
    to_user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='friendship_request_received')
    message = models.TextField(blank=True)
    created = models.DateTimeField(default=timezone.now)
    rejected = models.DateTimeField(blank=True, null=True)
    viewed = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Запрос дружбы'
        verbose_name_plural = 'Запросы дружбы'
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.from_user_id} friendship requested #{self.to_user_id}"

    def accept(self):
        """Принять дружеское отношение"""
        Friend.objects.created(from_user=self.from_user, to_user=self.to_user)

        Friend.objects.create(from_user=self.to_user, to_user=self.from_user)

        friendship_request_accepted.send(
            sender=self, from_user=self.from_user, to_user=self.to_user
        )

        self.delete()
        # Переброс кеша запросов - удаление кеша
        bust_cache('requests', self.to_user.pk)
        bust_cache('sent_requests', self.from_user.pk)
        # Перебор кэша обратных запросов - обратный запрос может быть удален
        bust_cache('requests', self.from_user.pk)
        bust_cache('sent_requests', self.to_user.pk)
        #Удаление кэш друзей - добавлены новые друзья
        bust_cache('friends', self.to_user.pk)
        bust_cache('friends', self.from_user.pk)

        return True

    def reject(self):
        """Отклонить входящий запрос дружбы"""
        self.rejected = timezone.now()
        self.save()

        friendship_request_rejected.send(sender=self)
        bust_cache("requests", self.to_user.pk)
        bust_cache("sent_requests", self.from_user.pk)
        return True

    def cancel(self):
        """Отклонить исходящий запрос дружбы"""
        friendship_request_canceled.send(sender=self)
        self.delete()
        bust_cache("requests", self.to_user.pk)
        bust_cache("sent_requests", self.from_user.pk)
        return True

    def mark_viewed(self):
        self.viewed = timezone.now()
        friendship_request_viewed.send(sender=self)
        self.save()
        bust_cache("requests", self.to_user.pk)
        return True


class FriendshipManager(models.Manager):
    """Менеджер дружественных отношений"""

    def friends(self, user):
        """Возвращает список всех друзей"""
        key = cache_key('friends', user.pk)
        friends = cache.get(key)

        if friends is None:
            queryset = Friend.objects.select_related('from_user').filter(to_user=user)
            friends = [u.from_user for u in queryset]
            cache.set(key, friends)

        return friends

    def requests(self, user):
        """Вoзвращает список всех запросов дружбы"""
        key = cache_key('requests', user.pk)
        requests = cache.get(key)

        if requests is None:
            queryset = Friend.objects.filter(to_user=user)
            queryset = self._friendship_request_select_related(queryset, 'from_user', 'to_user')
            requests = list(queryset)
            cache.set(key, requests)

            return requests

    def sent_requests(self, user):
        """Возвращает список всех запросов дружды от пользователя"""
        key = cache_key('sent_requests', user.pk)
        requests = cache.get(key)

        if requests is None:
            queryset = FriendshipRequest.objects.filter(from_user=user)
            queryset = self._friendship_request_select_related(queryset, 'from_user', 'to_user')
            requests = list(queryset)
            cache.set(key, requests)

            return requests

    def add_friend(self, from_user, to_user, message=None):
        """Создание запроса дружбы"""
        if from_user == to_user:
            raise ValidationError("Пользователь не может дружить сам с собой")

        if self.are_friends(from_user, to_user):
            raise AlreadyFriendsError("Пользователи уже друзья")

        if FriendshipRequest.objects.filter(
                from_user=from_user, to_user=to_user
        ).exists():
            raise AlreadyExistsError("Вы уже запрашивали дружбу у этого пользователя")

        if FriendshipRequest.objects.filter(
                from_user=to_user, to_user=from_user
        ).exists():
            raise AlreadyExistsError("Этот пользователь уже просил вас о дружбе")

        if message is None:
            message = ""

        request, created = FriendshipRequest.objects.get_or_create(
            from_user=from_user, to_user=to_user
        )

        if created is False:
            raise AlreadyExistsError("Дружба уже запрошена")

        if message:
            request.message = message
            request.save()

        bust_cache('requests', to_user.pk)
        bust_cache('sent_requests', from_user.pk)
        friendship_request_created.send(sender=request)

        return request

    def remove_friend(self, from_user, to_user):
        """Удаление дружественных отношений"""
        try:
            queryset = Friend.objects.filter(to_user__in=[to_user, from_user], from_user__in=[from_user, to_user]
                                             )

            if queryset:
                friendship_removed.send(
                    sender=queryset[0], from_user=from_user, to_user=to_user
                )
                queryset.delete()
                bust_cache("friends", to_user.pk)
                bust_cache("friends", from_user.pk)
                return True
            else:
                return False
        except Friend.DoesNotExist:
            return False

    def are_friends(self, user1, user2):
        """Являются ли эти два пользователя друзьями"""
        friends1 = cache.get(cache_key('friends', user1.pk))
        friends2 = cache.get(cache_key('friends', user2.pk))
        if friends1 and user2 in friends1:
            return True
        elif friends2 and user1 in friends2:
            return True
        else:
            try:
                Friend.objects.get(to_user=user1, from_user=user2)
                return True
            except Friend.DoesNotExist:
                return False

    def _friendship_request_select_related(self, queryset, *fields):
        _method = getattr(settings,
                          "FRIENDSHIP_MANAGER_FRIENDSHIP_REQUEST_SELECT_RELATED_STRATEGY",
                          "select_related",
                          )
        if _method == "select_related":
            queryset = queryset.select_related(*fields)
        elif _method == "prefetch_related":
            queryset = queryset.prefetch_related(*fields)
        return queryset

    def unread_requests(self, user):
        """Возвращает список непрочитанных запросов дружбы"""
        pass

    def unread_request_count(self, user):
        """Возвращает количество непрочитанных запросов на дружбу"""
        pass

    def read_requests(self, user):
        """Возвращает список прочитанных запросов дружбы"""
        pass

    def rejected_requests(self, user):
        """Возвращает список отклоненных запросов дружбы"""
        pass

    def unrejected_requests(self, user):
        """Все запросы дружбы, которые не были отклонены"""
        pass


class Friend(models.Model):
    """Модель дружественных отношений"""
    to_user = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='friends')
    from_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  related_name='_unused_friend_relation')
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = "Друг"
        verbose_name_plural = 'Друзья'
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f'User #{self.to_user_id} is friends with #{self.from_user_id}'

    def save(self, *args, **kwargs):
        #Нужно убедиться, чтобы пользоваетли не могли дружить сами с собой
        if self.to_user == self.from_user:
            raise ValidationError('Пользователи не могут дружить сами с собой')
        super().save(*args, **kwargs)


class FollowingManager(models.Manager):
    """Менеджер подписок"""

    def followers(self, user):
        """Возвращает список всех подписок"""
        key = cache_key('followers', user.pk)
        followers = cache.get(key)

        if followers is None:
            queryset = Follow.objects.filter(followee=user).select_related('follower')
            followers = [u.followers for u in queryset]
            cache.set(key, followers)

        return followers

    def following(self, follower, followee):
        """Создание связи 'follower' после 'followee'"""
        if follower == followee:
            raise ValidationError("Пользователь не может быть подписан сам на себя")

        relation, created = Follow.objects.get_or_create(
            follower=follower, followee=followee
        )

        if created is False:
            raise AlreadyExistsError(f"Пользователь '{follower}' уже подписан на '{followee}'")

        follower_created.send(sender=self, follower=follower)
        followee_created.send(sender=self, followee=followee)
        following_created.send(sender=self, following=relation)

        bust_cache('followers', followee.pk)
        bust_cache('following', follower.pk)

        return relation

    def add_follower(self, follower, followee):
        """Создать связб между подписчиком и подпиской"""
        if follower == followee:
            raise ValidationError("Пользователь не может подписаться сам на себя")

        relation, created = Follow.objects.get_or_create(
            follower=follower, followee=followee
        )

        if created is False:
            raise AlreadyExistsError(f"Пользователь '{follower}' уже подписан на '{followee}'")

        follower_created.send(sender=self, follower=follower)
        followee_created.send(sender=self, followee=followee)
        following_created.send(sender=self, following=relation)

        bust_cache('followers', followee.pk)
        bust_cache('following', follower.pk)

        return relation

    def remove_follower(self, follower, followee):
        """Удаление связи 'follower' после 'followee'"""
        try:
            relation = Follow.objects.get(follower=follower, followee=followee)
            follower_removed.send(sender=relation, follower=relation.follower)
            followee_removed.send(sender=relation, followee=relation.followee)
            following_removed.send(sender=relation, following=relation)
            relation.delete()
            bust_cache('followers', followee.pk)
            bust_cache('following', follower.pk)
            return True
        except Follow.DoesNotExist:
            return False

    def are_follower(self, follower, followee):
        pass

    def follows(self, follower, followee):
        """Следует ли подписчик за подпискойю?
           Шрамотное использование кешей, если такие существуют"""
        pass


class Follow(models.Model):
    """Модель подписок"""
    follower = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='following')
    followee = models.ForeignKey(User,
                                 on_delete=models.CASCADE,
                                 related_name='followers')
    created = models.DateTimeField(default=timezone.now)

    objects = FollowingManager()

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ("follower", "followee")

    def __str__(self):
        return f'User #{self.follower_id} follows #{self.followee_id}'

    def save(self, *args, **kwargs):
        # Убедиться, что пользователи не могут дружить сами с собой
        if self.follower == self.followee:
            raise ValidationError("Пользователи не могут дружить сами с собой")
        super().save(*args, **kwargs)


class BlockManager(models.Manager):
    """Менеджер для ограничений"""
    pass


class Block(models.Model):
    pass
