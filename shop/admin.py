from django.contrib import admin
from .models import Categorie, Pub, Produit, Review, Cluster


@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    """ Admin View for CategorieAdmin """
    list_display = ('name',)
    list_display_links = ('name',)
    list_per_page = 20
    ordering = ['name']
    search_fields = ['name', 'description', 'meta_description', 'meta_keywords']
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
    list_display = ('name', 'prix_reduit', 'prix', 'disponible', 'creation')
    list_display_links = ('name',)
    list_filter = ['disponible', 'creation', 'update']
    list_editable = ['prix_reduit', 'disponible']
    search_fields = ['name', 'description', 'meta_keywords', 'meta_description']
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
