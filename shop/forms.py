from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Produit


class ProduitAdminForm(forms.ModelForm):
    class Meta:
        model = Produit

    def clean_price(self):
        cleaned_data = super(ProduitAdminForm, self).clean()
        prix = cleaned_data.get("prix")
        prix_reduit = cleaned_data.get("prix_reduit")

        if prix_reduit > prix:
            raise forms.ValidationError('Erreur le prix marchant ne peut être supérieur au prix réduit')
        return cleaned_data
