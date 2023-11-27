from django import forms
from phonenumber_field.formfields import PhoneNumberField

from users.models import User, Profile


class EditUserInfoForm(forms.ModelForm):
    username = forms.CharField(max_length=64,
                               required=False,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = PhoneNumberField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']


class EditProfileInfoForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['img', 'first_name', 'last_name', 'bio', 'city', 'telegram_id', 'instagram_link']