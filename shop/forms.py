from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Produit


class ProduitAdminForm(forms.ModelForm):
    class Meta:
        model = Produit

    def clean_price(self):
        if self.cleaned_data['prix'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['prix']
