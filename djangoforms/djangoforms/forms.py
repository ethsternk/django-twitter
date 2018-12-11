from django import forms
from djangoforms.models import Author
import datetime


class AddTweet(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(AddTweet, self).__init__(*args, **kwargs)
        author = Author.objects.filter(user=user).first()
        self.fields['author'].choices = [(author.id, author.name)]

    body = forms.CharField(widget=forms.Textarea, max_length=280)
    author = forms.ChoiceField()


class SignupForm(forms.Form):
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
