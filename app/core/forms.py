from django.forms import ModelForm, TextInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import URLData


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]
        widgets = {
            "username": TextInput(attrs={"placeholder": "Username"}),
            "email": TextInput(attrs={"placeholder": "Email"}),
        }
