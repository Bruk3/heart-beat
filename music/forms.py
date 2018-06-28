from django.contrib.auth.models import User
from django import forms
from .models import Song

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PushSongForm(forms.ModelForm):
    class Meta:
        model = Song
        pushed_to = forms.IntegerField(label="Push the song for")
        fields = ['pushed_to', 'artist', 'title', 'source', 'description']