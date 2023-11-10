from django import template

from users.models import User

register = template.Library()

@register.simple_tag(takes_context=True)
def get_by_name(context, name):
    """Тег для поиска переменной в данном контексте"""
    return context[name]

@register.inclusion_tag('users/templatetags/profile.html')
def profile(user):
    """Тег чтобы захватить всё содержимое профиля"""
    return {'profile_context': User.objects.profile(user)}
