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
