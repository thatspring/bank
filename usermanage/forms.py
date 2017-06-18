from django import forms
from .models import Accounts
from django.utils.translation import ugettext as _
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from bank.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
class LoginForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
    def clean_username(self):
        data=self.cleaned_data['username']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Check User Name and Password'), code='invalid')
        return data
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user_profile = User.objects.get(username=username)
            if not username or not password or not hashers.check_password(password, user_profile.password):
                raise forms.ValidationError(_('Check User Name and Password'), code='invalid')


class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    username = forms.CharField(max_length=16)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        data = self.cleaned_data['email']
        user_exists = User.objects.filter(email=data).exists()
        if user_exists:
            raise forms.ValidationError(_('Email already exists'), code='invalid')
        return data
    def clean_username(self):
        data=self.cleaned_data['username']
        user_exists = User.objects.filter(username=data).exists()
        if user_exists:
            raise forms.ValidationError(_('UserName already exists'), code='invalid')
        return data
    def clean_password(self):
        data=self.cleaned_data['password']
        validate_password(password=data)
        return data
