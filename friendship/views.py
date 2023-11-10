from config import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from friendship.exceptions import AlreadyExistsError
from friendship.models import Block, Follow, Friend, FriendshipRequest
from users.models import User


def get_friendship_context_object_name():
    return getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_NAME", "user")


def get_friendship_context_object_list_name():
    return getattr(settings, "FRIENDSHIP_CONTEXT_OBJECT_LIST_NAME", "users")


@login_required(login_url='auth_login')
def all_users(request, template_name='friendship/all_users.html'):
    """Возвращает всех пользователей, исключая себя"""
    users = User.objects.all().exclude(username=request.user.username)

    return render(
        request, template_name, {get_friendship_context_object_list_name(): users}
    )


@login_required(login_url='auth_login')
def view_friends(request, username, template_name='friendship/user_list_friends.html'):
    """Показывает всех друзей пользователя"""
    user = get_object_or_404(User, username=username)
    friends = Friend.objects.friends(user)
    return render(
        request,
        template_name,
        {
            get_friendship_context_object_name(): user,
            'friendship_context_object_name': get_friendship_context_object_name(),
            'friends': friends,
        }
    )


@login_required(login_url='auth_login')
def friendship_add_friend(request, to_username, template_name='friendship/friend/add.html'):
    """Создание дружеского запроса FriendshipRequest"""
    context = {'to_username': to_username}

    if request.method == "POST":
        to_user = User.objects.get(username=to_username)
        from_user = request.user
        try:
            Friend.objects.add_friend(from_user, to_user)
        except AlreadyExistsError as error:
            context['errors'] = ["%s" % error]
        else:
            return redirect("friendship_request_list")
    return render(request, template_name, context)


@login_required(login_url='auth_login')
def friendship_accept(request, friendship_request_id):
    """Принять дружественное предложение"""
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_request_received, id=friendship_request_id
        )
        f_request.accept()

        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required(login_url='auth_login')
def friendship_reject(request, friendship_request_id):
    """Отклонить дружественное предложение"""
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_request_received, id=friendship_request_id
        )
        f_request.reject()

        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)


@login_required(login_url='auth_login')
def friendship_cancel(request, friendship_request_id):
    """Отменить дружественное предложение"""
    if request.method == 'POST':
        f_request = get_object_or_404(
            request.user.friendship_request_sent, id=friendship_request_id
        )
        f_request.cancel()

        return redirect('friendship_view_friends', username=request.user.username)

    return redirect('friendship_request_detail', friendship_request_id=friendship_request_id)



@login_required(login_url='auth_login')
def friendship_request_list(request, template_name='friendship/friend/requests_list.html'):
    """Показывает список всех дружественных запросов"""
    friendship_request = Friend.objects.requests(request.user)

    return render(request, template_name, {'requests': friendship_request})


@login_required(login_url='auth_login')
def friendship_request_detail(request, friendship_request_id, template_name='friendship/friend/request.html'):
    """Детальный просмотр запроса"""
    f_request = get_object_or_404(FriendshipRequest, id=friendship_request_id)

    return render(request, template_name, {'friendship_request': f_request})


