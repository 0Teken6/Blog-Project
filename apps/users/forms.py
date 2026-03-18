from .models import Profile
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from django import forms


class UserUpdateForm(ModelForm):
    email = forms.EmailField()
    class Meta:
        model = get_user_model()
        fields = (
            'username', 'email'
        )


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = (
            'profile_pic',
            'description'
        )
