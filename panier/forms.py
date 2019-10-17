# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _
CHOIX_QUANTITE_PRODUITS = [(i, str(i)) for i in range(1, 11)]


# Formulaire d'ajout de produit au panier
class AjouterProduitPanierForm(forms.Form):
    quantite = forms.TypedChoiceField(error_messages={'required': _('Please enter a number')},
        choices=CHOIX_QUANTITE_PRODUITS, coerce=int, label=_('Quantity'))

    update = forms.BooleanField(required=False, initial=False,
        widget=forms.HiddenInput)

    # Modification de l'affichage des variables
    quantite.widget.attrs.update({'class': 'custom-select custom-select-sm shadow-none border-0'})

    def clean(self):
        cleaned_data = super(AjouterProduitPanierForm, self).clean()
        quantite = cleaned_data.get('quantite')
        if not quantite:
            raise forms.ValidationError('Champs requis')
