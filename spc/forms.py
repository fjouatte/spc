from django import forms
from django.contrib import admin
from django.db import models
from spc.models import Rules, User
from tinymce.widgets import TinyMCE
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class RulesForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Rules
        fields = ('content', )


class RulesFormAdmin(admin.ModelAdmin):
    model = RulesForm
    fields = ('content', )
