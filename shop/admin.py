from django.contrib import admin
from .models import Categorie, Produit

# Enregistrement du modele de Catalogue sur la page d'administration
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    # sets up values for how admin site lists categories
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_description', 'meta_keywords']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    # sets values for how the admin site lists your products
    date_hierarchy = 'update'
    list_display = ['name', 'prix_reduit', 'prix', 'disponible', 'creation', 'update']
    list_display_links = ('name',)
    list_per_page = 50
    list_filter = ['disponible', 'creation', 'update']
    list_editable = ['prix_reduit', 'disponible']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
    exclude = ['creation', 'update']
    prepopulated_fields = {'slug': ('name',)}

    class Meta:
        model = Produit

    def clean_price(self):
        if self.cleaned_data['prix'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['prix']
