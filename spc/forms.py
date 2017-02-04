from django import forms
from django.contrib import admin
from spc.models import Rule, User, New
from tinymce.widgets import TinyMCE


class UnsubscribeForm(forms.Form):
    edition_id = forms.CharField()


class SubscribeForm(forms.Form):
    edition_id = forms.CharField()


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'login_trackmania')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Le mots de passe ne correspondent pas')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'login_trackmania')

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
