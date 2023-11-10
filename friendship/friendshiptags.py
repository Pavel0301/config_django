from django import template

from friendship.models import Friend, Follow

register = template.Library()

@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    """Тег для поиска переменной в данном контексте"""
    return context[name]

@register.inclusion_tag('friendship/templatetags/friends.html')
def friends(user):
    """Тег чтобы захватить всех друзей"""
    return {'friends': Friend.objects.friends(user)}

@register.inclusion_tag('friendship/templatetags/followers.html')
def followers(user):
    """Тег для захвата всех подписок на пользователя"""
    return {'followers': Follow.objects.followers(user)}

@register.inclusion_tag('friendship/templatetags/following.html')
def following(user):
    """Тег зазахватывающий всех пользователей,
       подписанных на пользователя"""
    return {'following': Follow.objects.following(user)}


@register.inclusion_tag('friendship/templatetags/friend_requests.html')
def friend_requests(user):
    """Тег захватывающий дружеские запросы к пользователю"""

    return {'friend_requests': Friend.objects.requests(user)}