from django.contrib import admin
from .models import Categorie, Produit

# Enregistrement du modele de Catalogue sur la page d'administration
@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    date_hierarchy = 'update'
    list_display = ['name', 'prix_reduit', 'prix', 'disponible', 'creation']
    list_filter = ['disponible', 'creation', 'update']
    list_editable = ['prix_reduit', 'disponible']
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',),}

    class Meta:
        model = Produit
