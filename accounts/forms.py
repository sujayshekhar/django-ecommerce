from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput, EmailInput, PasswordInput, HiddenInput
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField


class RegisterForm(UserCreationForm):
    """docstring for UserRegisterForm"""

    username = forms.CharField(label=_('last name'), label_suffix='',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    first_name = forms.CharField(label=_('first name'), label_suffix='',
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    telephone = forms.CharField(label=_('phone number'), label_suffix='', max_length=8,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        validators=[RegexValidator(r'^[0-9]+$')], localize=True)

    email = forms.EmailField(label=_('email'), label_suffix='', required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(label=_('password'), label_suffix='',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(label=_('confirm password'), label_suffix='',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username and password:
            raise forms.ValidationError(_('username does not exist.'))

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email', 'telephone', 'password1', 'password2')
