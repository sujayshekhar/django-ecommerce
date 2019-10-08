# -*- coding: utf-8 -*-

from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms import TextInput, EmailInput
from .models import Commande

CHOICES_VILLE = [("choose", _("Choose...")), ("Bouaké", "Bouaké"), ("Beoumi", "Beoumi"), ("Botro", "Botro")]


class FormCreationCommande(forms.ModelForm):
    telephone = forms.CharField(label_suffix='*', label=_("Mobile phone number"), required=True)
    ville = forms.ChoiceField(choices=CHOICES_VILLE, label=_('Choice a location'), label_suffix='*', required=True)

    # Modification de l'affichage des variables
    ville.widget.attrs.update({'class': 'custom-select shadow-none d-block w-100'})
    telephone.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Commande
        fields = ['first_name', 'last_name', 'telephone', 'adresse', 'ville']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'adresse': TextInput(attrs={'class': 'form-control'}),
        }
