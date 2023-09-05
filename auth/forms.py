from django import forms

from users.models import User


class UserRegForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )