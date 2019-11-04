# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import Marque, Categorie, Pub, Produit, Review, Cluster


@admin.register(Marque)
class MarqueAdmin(admin.ModelAdmin):
    """ Admin View for CategorieAdmin """
    list_display = ('name', 'is_active')
    list_display_links = ('name',)
    ordering = ['name']
    search_fields = ['name', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """ Admin View for CategorieAdmin """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'meta_keywords']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Pub)
class PubAdmin(admin.ModelAdmin):
    """ Admin View for PubAdmin """
    list_display = ['name', 'pub']

    class Meta:
        model = Pub


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    """ Admin View for ProduitAdmin """
    model = Produit
    date_hierarchy = 'update'
    list_display = ('marque', 'name', 'prix_reduit', 'prix', 'disponible', 'creation')
    list_display_links = ('name',)
    list_filter = ['marque', 'disponible', 'creation', 'update']
    list_editable = ['prix_reduit', 'disponible']
    search_fields = ['name', 'marque', 'meta_keywords']
    exclude = ['creation', 'update']
    prepopulated_fields = {'slug': ('name',)}

    def clean_price(self):
        if self.cleaned_data['prix'] <= 0:
            raise forms.ValidationError('Price must be greater than zero.')
        return self.cleaned_data['prix']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """ Admin View for ReviewAdmin """
    model = Review
    list_display = ('produit', 'rating', 'user_name', 'comment', 'pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']


@admin.register(Cluster)
class ClusterAdmin(admin.ModelAdmin):
    ''' Admin View for Cluster '''
    model = Cluster
    list_display = ['name', 'get_members']
