from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import *


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_artist = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_artist')

    def save(self, commit=True):
        if self.data.get('is_artist'):
            user = Artist()
            user.is_artist = True
        else:
            user = Listener()
            user.is_artist = False
        user.username = self.data['username']
        user.set_password(self.data['password1'])
        user.email = self.data['email']
        user.save()
        return user
