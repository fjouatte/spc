# coding: utf-8

from django import forms
from django.contrib import admin
from spc.models import Rule, New
from tinymce.widgets import TinyMCE


class UnsubscribeForm(forms.Form):
    edition_id = forms.CharField()


class SubscribeForm(forms.Form):
    edition_id = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

"""
class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='Email', widget=forms.EmailInput, )
    password = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'login_trackmania')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Le mots de passe ne correspondent pas')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError(u'Cette adresse mail est déjà utilisée')
        return email


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'login_trackmania')
"""


class NewForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    content_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = New
        fields = ('content', 'content_en', 'active')


class NewFormAdmin(admin.ModelAdmin):
    model = NewForm
    fields = ('content', 'content_en', 'active')

class RuleForm(forms.ModelForm):

    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    content_en = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Rule
        fields = ('content', 'content_en', 'active')


class RuleFormAdmin(admin.ModelAdmin):
    model = RuleForm
    fields = ('content', 'content_en', 'active')
