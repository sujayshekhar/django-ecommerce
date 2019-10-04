# -*- coding: utf-8 -*-

from django import forms
from django.forms import TextInput, EmailInput
from .models import Commande


class FormCreationCommande(forms.ModelForm):
    class Meta:
        model = Commande
        fields = ['first_name', 'last_name', 'email', 'telephone', 'adresse', 'ville']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'telephone': TextInput(attrs={'class': 'form-control'}),
            'adresse': TextInput(attrs={'class': 'form-control'}),
            'ville': TextInput(attrs={'class': 'form-control'})
        }
