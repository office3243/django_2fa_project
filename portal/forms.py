from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from . models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=14, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))


class SignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=14, widget=forms.TextInput(attrs={"class": "input-medium bfh-phone", "data-format": "+91dddddddddd"}))

    class Meta:
        model = User
        fields = ('phone', 'email', 'password1', 'password2',)
