# -*- coding: utf-8 -*-
from django.utils.translation import gettext_lazy as _
from django import forms

from .models import Produit, Review


class ProduitAdminForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['name']

    def clean_price(self):
        cleaned_data = super(ProduitAdminForm, self).clean()
        prix = cleaned_data.get("prix")
        prix_reduit = cleaned_data.get("prix_reduit")

        if prix_reduit > prix:
            raise forms.ValidationError('Erreur le prix marchant ne peut être supérieur au prix réduit')
        return cleaned_data

class ReviewAdminForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'rating', 'comment']
