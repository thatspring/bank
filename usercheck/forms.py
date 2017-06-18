from django import forms
from usermanage.models import Accounts
from django.utils.translation import ugettext as _
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from bank.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User


class CheckForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_username(self):
        data=self.cleaned_data['username']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('Check User Name and Password'), code='invalid')
        return data
    def clean(self):
        cleaned_data = super(CheckForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        if username and password:
            user_profile = User.objects.get(username=username)
            if not username or not password or not hashers.check_password(password, user_profile.password):
                raise forms.ValidationError(_('Check User Name and Password'), code='invalid')
