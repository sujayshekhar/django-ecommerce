# -*- coding: utf-8 -*-

from django import forms
from django.db import transaction
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class RegisterForm(UserCreationForm):
    """docstring for UserRegisterForm"""
    class Meta:
        model = User
        fields = ('pseudo', 'email', 'phone_number', 'password1', 'password2')

    @transaction.atomic
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class AuthenticateForm(AuthenticationForm):
    """docstring for AuthenticationForm"""

    class Meta:
        model = User
        fields = ('email', 'password')

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive',)

    def clean_username(self):
        user = self.cleaned_data.get('email')
        if not user and not password:
            raise forms.ValidationError(_('username does not exist.'))
