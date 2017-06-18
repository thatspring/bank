from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import hashers
from django.contrib.auth.password_validation import validate_password
from bank.settings import AUTH_PASSWORD_VALIDATORS
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
class TransferForm(forms.Form):
    money = forms.DecimalField(decimal_places=2, max_digits=20)
    comment = forms.CharField(max_length=255)
    target = forms.CharField(max_length=16)
    captcha=CaptchaField()
    def clean_target(self):
        data=self.cleaned_data['target']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('target not exists'), code='invalid')
        return data

class InfoForm(forms.Form):
    money = forms.DecimalField(decimal_places=2, max_digits=20)
    comment = forms.CharField(max_length=255)
    target = forms.CharField(max_length=16)
    def clean_target(self):
        data=self.cleaned_data['target']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('target not exists'), code='invalid')
        return data

class ShowForm(forms.Form):
    money = forms.DecimalField(decimal_places=2, max_digits=20)
    comment = forms.CharField(max_length=255)
    target = forms.CharField(max_length=16)
    transferID=forms.CharField(max_length=22)
    targetemail=forms.EmailField()
    def clean_target(self):
        data=self.cleaned_data['target']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('target not exists'), code='invalid')
        return data

class PayForm(forms.Form):
    money = forms.DecimalField(decimal_places=2, max_digits=20)
    comment = forms.CharField(max_length=255)
    target = forms.CharField(max_length=16)
    def clean_target(self):
        data=self.cleaned_data['target']
        user_exists = User.objects.filter(username=data).exists()
        if not user_exists:
            raise forms.ValidationError(_('target not exists'), code='invalid')
        return data