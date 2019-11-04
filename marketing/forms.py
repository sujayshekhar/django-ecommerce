# -*- coding: utf-8 -*-
#

from django import forms
from .models import EmailSubscribe


class EmailSubscribeForm(forms.ModelForm):
    """docstring for EmailSubscribe"""
    email = forms.EmailField( required=True,
        widget=forms.TextInput(attrs={"type":"email"})
    )

    class Meta:
        model = EmailSubscribe
        fields = ('email', )
