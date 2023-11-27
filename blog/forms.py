from django.forms import forms
from blog.models import Post


class PostCreateForm(forms.Form):

    class Meta:
        model = Post
        fields = ['title', 'text']