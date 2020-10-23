from django.contrib.auth.models import User
from django import forms
from . models import Writeup


class LoginForm(forms.Form):
    username = forms.CharField(max_length=250)
    password = forms.CharField(max_length=250, widget=forms.PasswordInput)


class RegForm(forms.Form):
    username = forms.CharField(max_length=250)
    first_name = forms.CharField(max_length=250)
    surname = forms.CharField(max_length=250)
    password = forms.CharField(widget=forms.PasswordInput)


class WriteupForm(forms.ModelForm):
    draft = forms.BooleanField(required=False)

    class Meta:
        model = Writeup
        exclude = ["author", 'likes', 'favourites', 'comments', 'views']
        widgets = {
            'draft': forms.CheckboxInput
        }


